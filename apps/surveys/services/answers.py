"""Сохранение ответов: проверки, пропуск вопроса, очистка устаревших ответов."""

from django.db import transaction
from django.utils import timezone

from apps.surveys.models import Question, RunAnswer, SurveyRun

from .engine import build_context, get_next_question, visible_questions


class AnswerError(Exception):
    """Ответ не принят. message показывается пользователю."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def _set_skipped(run, code, flag):
    skipped = [c for c in run.skipped_questions if c != code]
    if flag:
        skipped.append(code)
    run.skipped_questions = skipped
    run.save()


def _replace_answers(run, question, pairs):
    run.answers.filter(question=question).delete()
    RunAnswer.objects.bulk_create(
        [RunAnswer(run=run, question=question, option=option, value=value) for option, value in pairs]
    )
    if question.code in run.skipped_questions:
        _set_skipped(run, question.code, False)


def _save_skip(run, question):
    if question.is_required:
        raise AnswerError("Этот вопрос обязательный, его нельзя пропустить")
    run.answers.filter(question=question).delete()
    _set_skipped(run, question.code, True)


def _save_options(run, question, option_codes):
    codes = list(dict.fromkeys(option_codes or []))  # без повторов, порядок сохраняется
    if not codes:
        raise AnswerError("Выберите вариант ответа")
    if question.kind == Question.Kind.SINGLE and len(codes) > 1:
        raise AnswerError("Можно выбрать только один вариант")
    by_code = {o.code: o for o in question.options.all()}
    unknown = [c for c in codes if c not in by_code]
    if unknown:
        raise AnswerError("Нет такого варианта: " + ", ".join(unknown))
    if len(codes) > 1 and any(by_code[c].is_exclusive for c in codes):
        raise AnswerError("Этот вариант нельзя сочетать с другими")
    _replace_answers(run, question, [(by_code[c], "") for c in codes])


def _save_grid(run, question, grid):
    grid = grid or {}
    by_code = {o.code: o for o in question.options.all()}
    unknown = [c for c in grid if c not in by_code]
    if unknown:
        raise AnswerError("Нет такой строки: " + ", ".join(unknown))
    missing = [c for c in by_code if c not in grid]
    if missing:
        raise AnswerError("Не заполнены строки: " + ", ".join(missing))
    bad = [v for v in grid.values() if v not in RunAnswer.GridValue.values]
    if bad:
        raise AnswerError("Недопустимое значение: " + ", ".join(bad))
    _replace_answers(run, question, [(by_code[c], grid[c]) for c in by_code])


def _purge_hidden(run):
    """Удаляет ответы и пропуски для вопросов, которые после смены ответов стали скрытыми."""
    while True:
        visible_codes = {q.code for q in visible_questions(run, build_context(run))}
        hidden = run.answers.exclude(question__code__in=visible_codes)
        stale_skips = [c for c in run.skipped_questions if c not in visible_codes]
        if not hidden.exists() and not stale_skips:
            return
        hidden.delete()
        if stale_skips:
            run.skipped_questions = [c for c in run.skipped_questions if c in visible_codes]
            run.save()


def _update_status(run):
    if get_next_question(run) is None:
        run.status = SurveyRun.Status.COMPLETED
        run.completed_at = run.completed_at or timezone.now()
    else:
        run.status = SurveyRun.Status.IN_PROGRESS
        run.completed_at = None
    run.save()


@transaction.atomic
def submit_answer(run, question, options=None, grid=None, skip=False):
    """Принимает ответ на вопрос с кодом `question` и обновляет состояние прохождения."""
    target = run.scenario.questions.filter(code=question).first()
    if target is None:
        raise AnswerError("Такого вопроса нет в этом сценарии")
    if target.code not in {q.code for q in visible_questions(run)}:
        raise AnswerError("Этот вопрос сейчас не показывается")

    if skip:
        _save_skip(run, target)
    elif target.kind == Question.Kind.STATUS_GRID:
        _save_grid(run, target, grid)
    else:
        _save_options(run, target, options)

    _purge_hidden(run)
    _update_status(run)
    return run

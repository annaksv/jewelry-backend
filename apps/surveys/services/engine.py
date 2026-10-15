"""Движок опроса: какие вопросы видны и какой из них следующий."""

from .conditions import AnswerContext, evaluate


def build_context(run):
    """Собирает снимок ответов прохождения для проверки условий."""
    ctx = AnswerContext()
    for answer in run.answers.select_related("question", "option"):
        key = f"{answer.question.code}.{answer.option.code}"
        ctx.options.add(key)
        ctx.tags.update(answer.option.tags)
        ctx.answered.add(answer.question.code)
        if answer.value:
            ctx.values[key] = answer.value
    return ctx


def visible_questions(run, ctx=None):
    """Вопросы сценария, которые сейчас должны быть показаны, в порядке показа."""
    if ctx is None:
        ctx = build_context(run)
    return [q for q in run.scenario.questions.all() if evaluate(q.show_if, ctx)]


def get_next_question(run, ctx=None):
    """Первый видимый вопрос без ответа. None, если опрос закончен."""
    if ctx is None:
        ctx = build_context(run)
    for question in visible_questions(run, ctx):
        if question.code not in ctx.answered:
            return question
    return None


def get_progress(run, ctx=None):
    """Для надписи «ВОПРОС N ИЗ M». M может измениться по ходу ветвления."""
    if ctx is None:
        ctx = build_context(run)
    visible = visible_questions(run, ctx)
    answered = sum(1 for q in visible if q.code in ctx.answered)
    total = len(visible)
    return {"current": min(answered + 1, total), "total": total}

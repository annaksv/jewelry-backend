"""Состояние прохождения в том виде, в котором его получает frontend."""

from .engine import build_context, get_next_question, get_progress, visible_questions


def serialize_question(question, ctx):
    options = list(question.options.all())
    keys = {o.code: f"{question.code}.{o.code}" for o in options}
    return {
        "code": question.code,
        "step_label": question.step_label,
        "section_label": question.section_label,
        "text": question.text,
        "help_text": question.help_text,
        "kind": question.kind,
        "is_required": question.is_required,
        "options": [{"code": o.code, "label": o.label, "is_exclusive": o.is_exclusive} for o in options],
        "selected": [o.code for o in options if keys[o.code] in ctx.options],
        "grid_values": {o.code: ctx.values[keys[o.code]] for o in options if keys[o.code] in ctx.values},
        "is_skipped": question.code in ctx.skipped,
    }


def build_state(run, question_code=None):
    """Состояние прохождения. Если указан question_code, показывает именно этот вопрос."""
    ctx = build_context(run)
    visible = visible_questions(run, ctx)
    if question_code:
        question = next((q for q in visible if q.code == question_code), None)
        if question is None:
            raise LookupError("Такого вопроса нет или он сейчас не показывается")
    else:
        question = get_next_question(run, ctx)
    done = ctx.answered | ctx.skipped
    return {
        "id": run.id,
        "scenario": run.scenario.slug,
        "status": run.status,
        "question": serialize_question(question, ctx) if question else None,
        "progress": get_progress(run, ctx, question),
        "history": [q.code for q in visible if q.code in done],
    }

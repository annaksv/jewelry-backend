"""Загрузка сценариев из seed_data в базу."""

from django.db import transaction

from apps.surveys.models import AnswerOption, Question, Scenario


def _upsert(model, lookup, defaults, overwrite):
    if overwrite:
        return model.objects.update_or_create(**lookup, defaults=defaults)
    return model.objects.get_or_create(**lookup, defaults=defaults)


@transaction.atomic
def load_scenario(data, overwrite=False):
    """Создаёт сценарий, вопросы и варианты. Возвращает счётчики."""
    stats = {"created": 0, "existing": 0}

    def count(created):
        stats["created" if created else "existing"] += 1

    scenario, created = _upsert(
        Scenario,
        {"slug": data["slug"]},
        {k: data[k] for k in ("title", "description", "card_title", "card_subtitle", "order", "is_published")},
        overwrite,
    )
    count(created)

    for q_index, q in enumerate(data["questions"], start=1):
        question, created = _upsert(
            Question,
            {"scenario": scenario, "code": q["code"]},
            {
                "step_label": q["step_label"],
                "section_label": q["section_label"],
                "order": q_index,
                "text": q["text"],
                "help_text": q["help_text"],
                "kind": q["kind"],
                "is_required": q["is_required"],
                "show_if": q["show_if"],
            },
            overwrite,
        )
        count(created)
        for o_index, o in enumerate(q["options"], start=1):
            _, created = _upsert(
                AnswerOption,
                {"question": question, "code": o["code"]},
                {"label": o["label"], "order": o_index, "tags": o["tags"], "is_exclusive": o["is_exclusive"]},
                overwrite,
            )
            count(created)
    return stats

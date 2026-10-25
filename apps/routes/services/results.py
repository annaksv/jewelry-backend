"""Результаты сценариев «Оформить права на дизайн» и «Другой производитель предлагает похожие изделия».

В отличие от бизнес-маршрута, это не список шагов, а структура (карточки, этапы, способы защиты),
поэтому она целиком кладётся в Route.snapshot с полем kind. Всё содержимое и условия лежат в данных
(apps/routes/result_data/*.json), здесь только их применение. Модуль не зависит от Django.
"""

import json
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

from apps.surveys.services.conditions import evaluate

RESULT_SCHEMA_VERSION = 2
DATA_DIR = Path(__file__).resolve().parent.parent / "result_data"


@lru_cache(maxsize=None)
def _load(name):
    return json.loads((DATA_DIR / f"{name}.json").read_text(encoding="utf-8"))


def _answers(ctx):
    """{"objects": ["design", "jewelry"], "patent": ["yes"], ...}: ответы для «Изменить ответы» и отладки."""
    answers = {}
    for key in sorted(ctx.options):
        question, _, option = key.partition(".")
        answers.setdefault(question, []).append(option)
    return answers


def build_design_result(ctx):
    """Карточки по пяти ответам и все десять этапов со ссылками и файлами под материалы и способ продажи."""
    data = _load("design_rights")
    cards = [deepcopy(c["card"]) for c in data["cards"] if evaluate(c["condition"], ctx)]
    stages = []
    for source in data["stages"]:
        stage = {k: deepcopy(v) for k, v in source.items() if k != "variants"}
        variant = next((v for v in source["variants"] if evaluate(v["condition"], ctx)), None)
        stage["links"] = deepcopy(variant["links"]) if variant else []
        stage["downloads"] = deepcopy(variant["downloads"]) if variant else []
        stages.append(stage)
    return {"kind": "design", "answers": _answers(ctx), "cards": cards, "stages": stages}


def build_similar_products_result(ctx):
    """Маршрут по сочетанию прав. Для сочетаний, которых ещё нет в данных, возвращает состояние «в разработке»."""
    data = _load("similar_products")
    case = next((c for c in data["cases"] if evaluate(c["condition"], ctx)), None)
    goal = next((k.partition(".")[2] for k in sorted(ctx.options) if k.startswith("goal.")), None)

    result = {
        "kind": "similar_products",
        "answers": _answers(ctx),
        "caseId": case["id"] if case else None,
        "status": "ready" if case and case["ready"] else "in_development",
        "goal": goal,
        "questionOrder": case["questionOrder"] if case else [],
        "sectionArticleSlugs": case["sectionArticleSlugs"] if case else [],
        "message": None,
        "selectedMethodId": None,
        "route": None,
    }
    if result["status"] == "in_development":
        result["message"] = data["inDevelopmentMessage"]
        return result

    route = deepcopy(data["routes"][case["id"]])
    method = next((m for m in route["methods"] if m["actionId"] == goal), None)
    result["selectedMethodId"] = method["id"] if method else None
    result["route"] = route
    return result


RESULT_BUILDERS = {
    "design-rights": build_design_result,
    "similar-products": build_similar_products_result,
}

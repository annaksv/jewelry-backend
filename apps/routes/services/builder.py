"""Сборка маршрута из ответов прохождения."""

from django.db import transaction

from apps.surveys.models import SurveyRun
from apps.surveys.services.conditions import evaluate
from apps.surveys.services.engine import build_context

from apps.routes.models import Route, RouteRule
from apps.routes.services.results import RESULT_BUILDERS, RESULT_SCHEMA_VERSION

SCHEMA_VERSION = 1


class RunNotCompleted(Exception):
    """Опрос ещё не пройден до конца."""


def select_rules(run, ctx=None):
    """Правила, которые сработали для этого прохождения, в порядке показа."""
    if ctx is None:
        ctx = build_context(run)
    rules = (
        RouteRule.objects.filter(scenario=run.scenario)
        .select_related("block", "step_question")
        .prefetch_related("block__links")
        .order_by("position", "id")
    )
    selected, seen_keys = [], set()
    for rule in rules:
        if not evaluate(rule.condition, ctx):
            continue
        key = rule.block.dedupe_key
        if key:
            if key in seen_keys:
                continue
            seen_keys.add(key)
        promoted = bool(rule.promote_if) and evaluate(rule.promote_if, ctx)
        selected.append((promoted, rule))
    selected.sort(key=lambda item: not item[0])  # поднятые вперёд, остальной порядок сохраняется
    return [rule for _, rule in selected]


def serialize_step(rule, ctx=None):
    block = rule.block
    return {
        "number": rule.step_question.step_label if rule.step_question else "",
        "title": block.title,
        "body": block.body,
        "links": [
            {"label": l.label, "kind": l.kind, "target": l.target}
            for l in block.links.all()
            if not l.condition or (ctx is not None and evaluate(l.condition, ctx))
        ],
    }


@transaction.atomic
def get_or_build_route(run):
    """Возвращает маршрут. Пересобирает его только если пользователь менял ответы."""
    if run.status != SurveyRun.Status.COMPLETED:
        raise RunNotCompleted("Опрос ещё не завершён")

    route = Route.objects.filter(run=run).first()
    if route is not None and route.source_updated_at == run.updated_at:
        return route

    ctx = build_context(run)
    result_builder = RESULT_BUILDERS.get(run.scenario.slug)
    if result_builder is not None:
        snapshot, version = result_builder(ctx), RESULT_SCHEMA_VERSION
    else:
        snapshot = {"steps": [serialize_step(rule, ctx) for rule in select_rules(run, ctx)]}
        version = SCHEMA_VERSION
    if route is None:
        return Route.objects.create(
            run=run, user=run.user, scenario=run.scenario, snapshot=snapshot,
            schema_version=version, source_updated_at=run.updated_at,
        )
    route.snapshot = snapshot
    route.schema_version = version
    route.source_updated_at = run.updated_at
    route.save()
    return route


def route_payload(route):
    """Что отдаём frontend."""
    kind = route.snapshot.get("kind", "steps")
    return {
        "id": route.id,
        "run_id": route.run_id,
        "scenario": route.scenario.slug,
        "scenario_title": route.scenario.title,
        "schema_version": route.schema_version,
        "is_saved": route.user_id is not None,
        "kind": kind,
        "steps": route.snapshot.get("steps", []),
        "result": route.snapshot if kind != "steps" else None,
    }

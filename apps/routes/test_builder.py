import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from apps.routes.models import ContentBlock, RouteRule
from apps.routes.services.builder import RunNotCompleted, get_or_build_route, select_rules
from apps.surveys.models import AnswerOption, Question, Scenario, SurveyRun
from apps.surveys.services.access import hash_token
from apps.surveys.services.answers import submit_answer
from apps.surveys.services.conditions import AnswerContext, evaluate


@pytest.fixture
def seeded(db):
    call_command("seed_surveys")
    call_command("seed_routes")


def new_run(token=None):
    scenario = Scenario.objects.get(slug="open-business")
    return SurveyRun.objects.create(scenario=scenario, anon_token_hash=hash_token(token) if token else "")


def answer_all(run, steps):
    for code, options in steps:
        submit_answer(run, code, options=options)


SERVICES_PATH = [("q1", ["none"]), ("q2", ["services"]), ("q6", ["online"]), ("q7", ["new_only"]),
                 ("q8", ["own"]), ("q9", ["no"]), ("q10", ["none"])]

FULL_PATH = [("q1", ["ip"]), ("q2", ["produce_sell"]), ("q3", ["self"]), ("q4", ["metal", "stone"]),
             ("q5", ["ru"]), ("q6", ["online", "marketplace"]), ("q7", ["client"]), ("q7_1", ["repair"]),
             ("q8", ["both"]), ("q9", ["unknown"]), ("q10", ["yes"])]


def test_route_requires_completed_run(seeded):
    run = new_run("tok")
    client = APIClient()
    response = client.get(f"/api/v1/runs/{run.id}/route/", HTTP_X_RUN_TOKEN="tok")
    assert response.status_code == 409
    with pytest.raises(RunNotCompleted):
        get_or_build_route(run)


def test_services_path_route(seeded):
    run = new_run()
    answer_all(run, SERVICES_PATH)
    steps = get_or_build_route(run).snapshot["steps"]
    assert [s["number"] for s in steps] == ["1", "2", "6", "7", "8", "9", "10"]
    assert steps[0]["title"] == "Зарегистрируйте бизнес"
    assert steps[0]["links"][0]["kind"] == "article"


def test_full_path_route(seeded):
    run = new_run()
    answer_all(run, FULL_PATH)
    codes = [rule.block.code for rule in select_rules(run)]
    assert codes == [
        "biz.q1.ip", "biz.q2.produce_sell", "biz.q3.self", "biz.q4.metal_stone", "biz.q5.ru",
        "biz.q6.online", "biz.q6.marketplace", "biz.q7.client", "biz.q7_1.repair", "biz.q8.both",
        "biz.q9.unknown", "biz.q10.yes",
    ]
    steps = get_or_build_route(run).snapshot["steps"]
    assert [s["number"] for s in steps] == ["1", "2", "3", "4", "5", "6", "6", "7", "7.1", "8", "9", "10"]


def test_snapshot_survives_text_edit_until_answers_change(seeded):
    run = new_run()
    answer_all(run, SERVICES_PATH)
    route = get_or_build_route(run)

    ContentBlock.objects.filter(code="biz.q1.none").update(body="НОВЫЙ ТЕКСТ")
    again = get_or_build_route(run)
    assert not any(s["body"] == "НОВЫЙ ТЕКСТ" for s in again.snapshot["steps"])

    submit_answer(run, "q10", options=["yes"])  # пользователь изменил ответ
    rebuilt = get_or_build_route(run)
    assert any(s["body"] == "НОВЫЙ ТЕКСТ" for s in rebuilt.snapshot["steps"])
    assert rebuilt.pk == route.pk


def test_dedupe_and_promote(db):
    scenario = Scenario.objects.create(slug="t", title="T", is_published=True)
    question = Question.objects.create(scenario=scenario, code="q1", order=1, text="?")
    AnswerOption.objects.create(question=question, code="a", label="A", order=1)
    b1 = ContentBlock.objects.create(scenario=scenario, code="b1", title="B1")
    b2 = ContentBlock.objects.create(scenario=scenario, code="b2", title="B2")
    b3 = ContentBlock.objects.create(scenario=scenario, code="b3", title="B3", dedupe_key="k")
    b4 = ContentBlock.objects.create(scenario=scenario, code="b4", title="B4", dedupe_key="k")
    RouteRule.objects.create(scenario=scenario, block=b1, position=10)
    RouteRule.objects.create(scenario=scenario, block=b2, position=20, promote_if={"option": "q1.a"})
    RouteRule.objects.create(scenario=scenario, block=b3, position=30)
    RouteRule.objects.create(scenario=scenario, block=b4, position=40)

    run = SurveyRun.objects.create(scenario=scenario)
    submit_answer(run, "q1", options=["a"])
    titles = [s["title"] for s in get_or_build_route(run).snapshot["steps"]]
    assert titles == ["B2", "B1", "B3"]


def test_route_api_returns_steps(seeded):
    run = new_run("tok")
    answer_all(run, SERVICES_PATH)
    response = APIClient().get(f"/api/v1/runs/{run.id}/route/", HTTP_X_RUN_TOKEN="tok")
    assert response.status_code == 200
    assert response.data["scenario"] == "open-business"
    assert response.data["is_saved"] is False
    assert len(response.data["steps"]) == 7
    assert response.data["steps"][0]["number"] == "1"


def test_seed_routes_is_idempotent_and_keeps_edits(seeded):
    assert ContentBlock.objects.count() == 40
    assert RouteRule.objects.count() == 40
    ContentBlock.objects.filter(code="biz.q1.ip").update(body="Правка юриста")
    call_command("seed_routes")
    assert ContentBlock.objects.count() == 40
    assert RouteRule.objects.count() == 40
    assert ContentBlock.objects.get(code="biz.q1.ip").body == "Правка юриста"


def _leaves(condition, key):
    if isinstance(condition, dict):
        for name, value in condition.items():
            if name == key and isinstance(value, str):
                yield value
            else:
                yield from _leaves(value, key)
    elif isinstance(condition, list):
        for item in condition:
            yield from _leaves(item, key)


def test_all_route_conditions_are_valid_and_reference_existing_data(seeded):
    options = AnswerOption.objects.select_related("question")
    valid_options = {f"{o.question.code}.{o.code}" for o in options}
    valid_tags = {tag for o in options for tag in o.tags}
    for rule in RouteRule.objects.all():
        for condition in (rule.condition, rule.promote_if):
            if condition:
                evaluate(condition, AnswerContext())
                assert set(_leaves(condition, "option")) <= valid_options, rule.block.code
                assert set(_leaves(condition, "tag")) <= valid_tags, rule.block.code

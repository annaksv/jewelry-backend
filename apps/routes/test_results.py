import itertools
import json

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APIClient

from apps.routes.models import Route
from apps.routes.services.builder import get_or_build_route
from apps.routes.services.results import _load, build_design_result, build_similar_products_result
from apps.surveys.models import Scenario, SurveyRun
from apps.surveys.seed_data.design_rights import SCENARIO as DESIGN
from apps.surveys.seed_data.similar_products import SCENARIO as SIMILAR
from apps.surveys.services.access import hash_token
from apps.surveys.services.answers import submit_answer
from apps.surveys.services.conditions import AnswerContext, evaluate

PATENT_CLAIM = "industrial-design-claim"


# ---------- вспомогательное: контекст ответов без базы данных ----------

def ctx_for(scenario, answers):
    ctx = AnswerContext()
    questions = {q["code"]: q for q in scenario["questions"]}
    for code, options in answers.items():
        ctx.answered.add(code)
        for option in options:
            ctx.options.add(f"{code}.{option}")
            ctx.tags.update(next(o for o in questions[code]["options"] if o["code"] == option)["tags"])
    return ctx


def visible_answers(scenario, choices):
    """Оставляет ответы только на те вопросы, которые движок показал бы при таких ответах."""
    answers = {}
    for q in scenario["questions"]:
        if evaluate(q["show_if"], ctx_for(scenario, answers)):
            answers[q["code"]] = choices[q["code"]]
    return answers


# ---------- чистые тесты: все комбинации ответов ----------

def test_design_every_combination_gives_five_cards_and_ten_stages():
    combos = itertools.product(["yes", "no", "unknown"], ["registered", "learn", "unneeded"],
                               ["online", "shop", "none"], ["yes", "no"], ["precious", "jewelry", "unknown"])
    for rights, patent, sales, suppliers, materials in combos:
        answers = {"rights": [rights], "patent": [patent], "sales": [sales],
                   "suppliers": [suppliers], "materials": [materials]}
        result = build_design_result(ctx_for(DESIGN, answers))
        assert [c["item"]["questionId"] for c in result["cards"]] == \
            ["rights", "patent", "sales", "suppliers", "materials"]
        assert len(result["stages"]) == 10

        no_sale = sales == "none"
        sales_card = result["cards"][2]
        assert (sales_card["item"]["stages"] == []) == no_sale
        assert (sales_card["fallbackText"] is not None) == no_sale

        needs_catalog = suppliers == "no" and materials == "precious"
        supplier_card = result["cards"][3]
        assert supplier_card["item"]["suppliers"] == needs_catalog
        assert any(link["href"] == "/suppliers" for link in supplier_card["links"]) == needs_catalog

        downloads = [d["href"] for s in result["stages"] for d in s["downloads"]]
        assert downloads == ([] if materials == "jewelry"
                             else ["/documents/contracts/jewelry-manufacturing-contract.docx"])


def test_similar_exactly_one_case_matches_every_combination():
    objects_sets = [c for n in range(1, 6)
                    for c in itertools.combinations(["jewelry", "design", "photos", "name", "logo"], n)]
    cases = _load("similar_products")["cases"]
    ready_ids = set()
    for objects in objects_sets:
        for patent, trademark, goal in itertools.product(["yes", "no"], ["yes", "no"], ["evaluate", "stop", "court"]):
            choices = {"objects": list(objects), "patent": [patent], "trademark": [trademark],
                       "evidence": ["file"], "goal": [goal]}
            ctx = ctx_for(SIMILAR, visible_answers(SIMILAR, choices))
            matches = [c["id"] for c in cases if evaluate(c["condition"], ctx)]
            assert len(matches) == 1, (objects, patent, trademark, matches)
            result = build_similar_products_result(ctx)
            if result["status"] == "ready":
                ready_ids.add(result["caseId"])
                assert result["selectedMethodId"] == f"{result['route']['routeId']}-{goal}"
            else:
                assert result["route"] is None and result["message"]
    assert len(ready_ids) == 9


def test_patent_claim_only_in_routes_that_require_a_patent():
    data = _load("similar_products")
    with_patent = {"patent", "patent-copyright", "patent-trademark", "all-rights"}
    for route_id, route in data["routes"].items():
        assert (PATENT_CLAIM in json.dumps(route)) == (route_id in with_patent), route_id


def test_every_ready_route_has_seven_methods_and_each_goal_is_selectable():
    data = _load("similar_products")
    assert len(data["routes"]) == 9
    goals = ["evaluate", "record", "stop", "compensate", "challenge", "court", "learn"]
    for route in data["routes"].values():
        assert [m["actionId"] for m in route["methods"]] == goals
        assert route["blocks"]


# ---------- с базой: настоящий движок, API, сохранение в кабинет ----------

DESIGN_PATH = [("rights", ["yes"]), ("patent", ["learn"]), ("sales", ["online"]),
               ("suppliers", ["no"]), ("materials", ["precious"])]
SIMILAR_PATENT_PATH = [("objects", ["jewelry"]), ("patent", ["yes"]), ("goal", ["stop"])]


@pytest.fixture
def seeded(db):
    call_command("seed_surveys")
    call_command("seed_routes")


def make_user(email="a@example.com"):
    return get_user_model().objects.create_user(email=email, password="Str0ng-pass-123")


def client_for(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


def completed_run(slug, path, token="tok"):
    run = SurveyRun.objects.create(scenario=Scenario.objects.get(slug=slug), anon_token_hash=hash_token(token))
    for code, options in path:
        submit_answer(run, code, options=options)
    return run


def test_design_route_snapshot(seeded):
    route = get_or_build_route(completed_run("design-rights", DESIGN_PATH))
    assert route.schema_version == 2
    assert route.snapshot["kind"] == "design"
    assert route.snapshot["answers"]["materials"] == ["precious"]
    assert len(route.snapshot["cards"]) == 5
    assert len(route.snapshot["stages"]) == 10


def test_design_route_api_shape(seeded):
    run = completed_run("design-rights", DESIGN_PATH)
    response = APIClient().get(f"/api/v1/runs/{run.id}/route/", HTTP_X_RUN_TOKEN="tok")
    assert response.status_code == 200
    assert response.data["kind"] == "design"
    assert response.data["steps"] == []
    assert response.data["result"]["cards"][3]["item"]["suppliers"] is True
    assert response.data["is_saved"] is False


def test_business_route_keeps_steps_shape(seeded):
    path = [("q1", ["none"]), ("q2", ["services"]), ("q6", ["online"]), ("q7", ["new_only"]),
            ("q8", ["own"]), ("q9", ["no"]), ("q10", ["none"])]
    run = completed_run("open-business", path)
    response = APIClient().get(f"/api/v1/runs/{run.id}/route/", HTTP_X_RUN_TOKEN="tok")
    assert response.data["kind"] == "steps"
    assert response.data["result"] is None
    assert len(response.data["steps"]) == 7
    assert response.data["schema_version"] == 1


def test_similar_route_with_patent(seeded):
    route = get_or_build_route(completed_run("similar-products", SIMILAR_PATENT_PATH))
    result = route.snapshot
    assert result["kind"] == "similar_products"
    assert result["status"] == "ready"
    assert result["caseId"] == "patent"
    assert result["selectedMethodId"] == "patent-stop"
    assert len(result["route"]["methods"]) == 7
    assert PATENT_CLAIM in str(result["route"])


def test_similar_route_without_patent_has_no_patent_claim(seeded):
    path = [("objects", ["jewelry"]), ("patent", ["no"]), ("goal", ["stop"])]
    result = get_or_build_route(completed_run("similar-products", path)).snapshot
    assert result["caseId"] == "no-patent"
    assert PATENT_CLAIM not in str(result["route"])


def test_similar_route_in_development(seeded):
    path = [("objects", ["jewelry", "design", "name"]), ("patent", ["no"]), ("trademark", ["no"]),
            ("evidence", ["file"]), ("goal", ["learn"])]
    result = get_or_build_route(completed_run("similar-products", path)).snapshot
    assert result["status"] == "in_development"
    assert result["route"] is None
    assert result["message"]


def test_changing_answers_rebuilds_the_result(seeded):
    run = completed_run("similar-products", SIMILAR_PATENT_PATH)
    assert get_or_build_route(run).snapshot["caseId"] == "patent"
    submit_answer(run, "patent", options=["no"])
    assert get_or_build_route(run).snapshot["caseId"] == "no-patent"


@pytest.mark.parametrize("slug, path", [("design-rights", DESIGN_PATH), ("similar-products", SIMILAR_PATENT_PATH)])
def test_saved_result_equals_shown_result(seeded, slug, path):
    user = make_user()
    run = completed_run(slug, path)
    shown = APIClient().get(f"/api/v1/runs/{run.id}/route/", HTTP_X_RUN_TOKEN="tok").data["result"]

    claimed = client_for(user).post(f"/api/v1/runs/{run.id}/claim/", HTTP_X_RUN_TOKEN="tok")
    assert claimed.status_code == 200
    assert claimed.data["is_saved"] is True

    route = Route.objects.get(run=run)
    detail = client_for(user).get(f"/api/v1/routes/{route.id}/")
    assert detail.status_code == 200
    assert detail.data["result"] == shown
    assert detail.data["kind"] == shown["kind"]

    listing = client_for(user).get("/api/v1/me/routes/").data["results"]
    assert listing[0]["scenario"] == slug
    assert listing[0]["kind"] == shown["kind"]
    assert listing[0]["steps_count"] == 0

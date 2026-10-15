import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.surveys.models import AnswerOption, Question, RunAnswer, Scenario, SurveyRun


def make_options(question, items):
    for i, item in enumerate(items, start=1):
        code, exclusive = (item, False) if isinstance(item, str) else item
        AnswerOption.objects.create(question=question, code=code, label=code, order=i, is_exclusive=exclusive)


@pytest.fixture
def scenario(db):
    sc = Scenario.objects.create(slug="demo", title="Демо", is_published=True)
    q1 = Question.objects.create(scenario=sc, code="q1", order=1, text="Кто вы?", step_label="1")
    make_options(q1, ["ip", "llc"])
    q2 = Question.objects.create(scenario=sc, code="q2", order=2, text="Только для ИП", show_if={"option": "q1.ip"})
    make_options(q2, ["a"])
    q3 = Question.objects.create(scenario=sc, code="q3", order=3, text="Необязательный",
                                 kind=Question.Kind.MULTI, is_required=False)
    make_options(q3, ["x", "y", ("none", True)])
    return sc


@pytest.fixture
def grid_scenario(db):
    sc = Scenario.objects.create(slug="grid", title="Таблица", is_published=True)
    q = Question.objects.create(scenario=sc, code="g", order=1, text="Что готово", kind=Question.Kind.STATUS_GRID)
    make_options(q, ["row1", "row2"])
    return sc


def start(slug="demo"):
    client = APIClient()
    response = client.post("/api/v1/runs/", {"scenario": slug}, format="json")
    assert response.status_code == 201
    return client, response.data["id"], response.data["anon_token"]


def answer(client, run_id, token, payload):
    return client.post(f"/api/v1/runs/{run_id}/answers/", payload, format="json", HTTP_X_RUN_TOKEN=token)


def test_scenario_list_only_published(scenario):
    Scenario.objects.create(slug="draft", title="Черновик", is_published=False)
    response = APIClient().get("/api/v1/scenarios/")
    assert response.status_code == 200
    assert [s["slug"] for s in response.data] == ["demo"]


def test_guest_can_start_run_and_gets_token(scenario):
    client, run_id, token = start()
    assert token
    response = client.get(f"/api/v1/runs/{run_id}/", HTTP_X_RUN_TOKEN=token)
    assert response.status_code == 200
    assert response.data["question"]["code"] == "q1"
    assert response.data["progress"] == {"current": 1, "total": 2}


def test_run_detail_requires_token(scenario):
    _, run_id, token = start()
    other = APIClient()
    assert other.get(f"/api/v1/runs/{run_id}/").status_code == 404
    assert other.get(f"/api/v1/runs/{run_id}/", HTTP_X_RUN_TOKEN="wrong").status_code == 404


def test_answer_moves_to_next_question(scenario):
    client, run_id, token = start()
    response = answer(client, run_id, token, {"question": "q1", "options": ["ip"]})
    assert response.status_code == 200
    assert response.data["question"]["code"] == "q2"
    assert response.data["history"] == ["q1"]


def test_wrong_option_rejected(scenario):
    client, run_id, token = start()
    response = answer(client, run_id, token, {"question": "q1", "options": ["nope"]})
    assert response.status_code == 400


def test_hidden_question_rejected(scenario):
    client, run_id, token = start()
    answer(client, run_id, token, {"question": "q1", "options": ["llc"]})
    response = answer(client, run_id, token, {"question": "q2", "options": ["a"]})
    assert response.status_code == 400


def test_exclusive_option_cannot_be_combined(scenario):
    client, run_id, token = start()
    answer(client, run_id, token, {"question": "q1", "options": ["llc"]})
    response = answer(client, run_id, token, {"question": "q3", "options": ["x", "none"]})
    assert response.status_code == 400


def test_required_question_cannot_be_skipped(scenario):
    client, run_id, token = start()
    response = answer(client, run_id, token, {"question": "q1", "skip": True})
    assert response.status_code == 400


def test_optional_question_can_be_skipped_and_run_completes(scenario):
    client, run_id, token = start()
    answer(client, run_id, token, {"question": "q1", "options": ["llc"]})
    response = answer(client, run_id, token, {"question": "q3", "skip": True})
    assert response.status_code == 200
    assert response.data["status"] == "completed"
    assert response.data["question"] is None


def test_changing_answer_removes_answers_to_hidden_questions(scenario):
    client, run_id, token = start()
    answer(client, run_id, token, {"question": "q1", "options": ["ip"]})
    answer(client, run_id, token, {"question": "q2", "options": ["a"]})
    answer(client, run_id, token, {"question": "q3", "skip": True})
    assert RunAnswer.objects.filter(run_id=run_id, question__code="q2").count() == 1

    response = answer(client, run_id, token, {"question": "q1", "options": ["llc"]})
    assert response.status_code == 200
    assert RunAnswer.objects.filter(run_id=run_id, question__code="q2").count() == 0
    assert SurveyRun.objects.get(pk=run_id).status == SurveyRun.Status.COMPLETED


def test_authenticated_user_owns_run(scenario):
    user = get_user_model().objects.create_user(email="a@example.com", password="Str0ng-pass-123")
    client = APIClient()
    client.force_authenticate(user)
    response = client.post("/api/v1/runs/", {"scenario": "demo"}, format="json")
    assert response.status_code == 201
    assert "anon_token" not in response.data
    run = SurveyRun.objects.get(pk=response.data["id"])
    assert run.user == user
    assert client.get(f"/api/v1/runs/{run.id}/").status_code == 200


def test_view_previous_question_with_saved_answer(scenario):
    client, run_id, token = start()
    answer(client, run_id, token, {"question": "q1", "options": ["ip"]})
    response = client.get(f"/api/v1/runs/{run_id}/?question=q1", HTTP_X_RUN_TOKEN=token)
    assert response.status_code == 200
    assert response.data["question"]["code"] == "q1"
    assert response.data["question"]["selected"] == ["ip"]


def test_grid_valid_completes(grid_scenario):
    client, run_id, token = start("grid")
    response = answer(client, run_id, token, {"question": "g", "grid": {"row1": "ready", "row2": "unknown"}})
    assert response.status_code == 200
    assert response.data["status"] == "completed"


def test_grid_missing_row_rejected(grid_scenario):
    client, run_id, token = start("grid")
    response = answer(client, run_id, token, {"question": "g", "grid": {"row1": "ready"}})
    assert response.status_code == 400

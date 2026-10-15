import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APIClient

from apps.routes.models import ContentBlock, Route
from apps.routes.services.builder import get_or_build_route
from apps.surveys.models import Scenario, SurveyRun
from apps.surveys.services.access import hash_token
from apps.surveys.services.answers import submit_answer

SERVICES_PATH = [("q1", ["none"]), ("q2", ["services"]), ("q7", ["new_only"]),
                 ("q8", ["own"]), ("q9", ["no"]), ("q10", ["none"])]


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


def completed_run(token="tok"):
    run = SurveyRun.objects.create(scenario=Scenario.objects.get(slug="open-business"),
                                   anon_token_hash=hash_token(token))
    for code, options in SERVICES_PATH:
        submit_answer(run, code, options=options)
    return run


def claim(client, run, token="tok"):
    return client.post(f"/api/v1/runs/{run.id}/claim/", HTTP_X_RUN_TOKEN=token)


def test_claim_requires_login(seeded):
    run = completed_run()
    response = APIClient().post(f"/api/v1/runs/{run.id}/claim/", HTTP_X_RUN_TOKEN="tok")
    assert response.status_code == 401


def test_claim_binds_run_and_route_and_kills_guest_token(seeded):
    user = make_user()
    run = completed_run()
    response = claim(client_for(user), run)
    assert response.status_code == 200
    assert response.data["is_saved"] is True
    assert response.data["route_id"] is not None

    run.refresh_from_db()
    assert run.user == user
    assert run.anon_token_hash == ""
    assert Route.objects.get(run=run).user == user
    assert APIClient().get(f"/api/v1/runs/{run.id}/route/", HTTP_X_RUN_TOKEN="tok").status_code == 404


def test_claim_does_not_rebuild_snapshot(seeded):
    user = make_user()
    run = completed_run()
    get_or_build_route(run)
    ContentBlock.objects.filter(code="biz.q1.none").update(body="НОВЫЙ ТЕКСТ")
    claim(client_for(user), run)
    route = Route.objects.get(run=run)
    assert not any(step["body"] == "НОВЫЙ ТЕКСТ" for step in route.snapshot["steps"])


def test_claim_unfinished_run_then_finish(seeded):
    user = make_user()
    run = SurveyRun.objects.create(scenario=Scenario.objects.get(slug="open-business"),
                                   anon_token_hash=hash_token("tok"))
    submit_answer(run, "q1", options=["none"])
    client = client_for(user)

    response = claim(client, run)
    assert response.status_code == 200
    assert response.data["route_id"] is None
    assert response.data["status"] == "in_progress"

    run.refresh_from_db()
    for code, options in SERVICES_PATH[1:]:
        submit_answer(run, code, options=options)
    assert client.get(f"/api/v1/runs/{run.id}/route/").status_code == 200
    assert Route.objects.get(run=run).user == user


def test_cannot_claim_someone_elses_run(seeded):
    run = completed_run()
    claim(client_for(make_user("a@example.com")), run)
    response = claim(client_for(make_user("b@example.com")), run)
    assert response.status_code == 404


def test_my_routes_lists_only_own(seeded):
    a, b = make_user("a@example.com"), make_user("b@example.com")
    run_a, run_b = completed_run("ta"), completed_run("tb")
    claim(client_for(a), run_a, "ta")
    claim(client_for(b), run_b, "tb")

    response = client_for(a).get("/api/v1/me/routes/")
    assert response.status_code == 200
    ids = [item["id"] for item in response.data["results"]]
    assert ids == [str(Route.objects.get(run=run_a).id)]
    assert response.data["results"][0]["steps_count"] == 6


def test_saved_route_detail_only_for_owner(seeded):
    a, b = make_user("a@example.com"), make_user("b@example.com")
    run = completed_run()
    claim(client_for(a), run)
    route = Route.objects.get(run=run)

    ok = client_for(a).get(f"/api/v1/routes/{route.id}/")
    assert ok.status_code == 200
    assert ok.data["run_id"] == str(run.id)
    assert ok.data["is_saved"] is True
    assert len(ok.data["steps"]) == 6
    assert client_for(b).get(f"/api/v1/routes/{route.id}/").status_code == 404


def test_me_endpoint(db):
    assert APIClient().get("/api/v1/me/").status_code == 401
    response = client_for(make_user()).get("/api/v1/me/")
    assert response.status_code == 200
    assert response.data["email"] == "a@example.com"

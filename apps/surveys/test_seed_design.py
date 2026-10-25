import pytest
from django.core.management import call_command

from apps.surveys.models import AnswerOption, Question, Scenario, SurveyRun
from apps.surveys.services.answers import AnswerError, submit_answer
from apps.surveys.services.engine import get_next_question, visible_questions

SLUG = "design-rights"
PATH = [("rights", ["yes"]), ("patent", ["learn"]), ("sales", ["online"]),
        ("suppliers", ["no"]), ("materials", ["precious"])]


@pytest.fixture
def run(db):
    call_command("seed_surveys")
    return SurveyRun.objects.create(scenario=Scenario.objects.get(slug=SLUG))


def test_seed_loads_design_scenario(run):
    scenario = run.scenario
    assert scenario.is_published
    assert [q.code for q in scenario.questions.all()] == ["rights", "patent", "sales", "suppliers", "materials"]
    assert all(q.kind == "single" and q.is_required for q in scenario.questions.all())
    assert AnswerOption.objects.filter(question__scenario=scenario).count() == 14


def test_every_question_is_always_shown_in_order(run):
    assert [q.code for q in visible_questions(run)] == [code for code, _ in PATH]


def test_full_path_completes(run):
    for code, options in PATH:
        assert get_next_question(run).code == code
        submit_answer(run, code, options=options)
    assert get_next_question(run) is None
    run.refresh_from_db()
    assert run.status == SurveyRun.Status.COMPLETED


def test_questions_are_required_and_single_choice(run):
    with pytest.raises(AnswerError):
        submit_answer(run, "rights", skip=True)
    with pytest.raises(AnswerError):
        submit_answer(run, "rights", options=["yes", "no"])


def test_old_design_scenario_is_not_reloaded(run):
    assert not Scenario.objects.filter(slug="design-to-sale", is_published=True).exists()


def test_reseed_does_not_duplicate(run):
    call_command("seed_surveys")
    assert Question.objects.filter(scenario__slug=SLUG).count() == 5

import pytest
from django.core.management import call_command

from apps.surveys.models import AnswerOption, Question, RunAnswer, Scenario, SurveyRun
from apps.surveys.services.answers import AnswerError, submit_answer
from apps.surveys.services.engine import get_next_question, visible_questions

SLUG = "similar-products"


@pytest.fixture
def run(db):
    call_command("seed_surveys")
    return SurveyRun.objects.create(scenario=Scenario.objects.get(slug=SLUG))


def codes(run):
    return [q.code for q in visible_questions(run)]


def test_seed_loads_similar_scenario(run):
    scenario = run.scenario
    assert scenario.is_published
    assert [q.code for q in scenario.questions.all()] == ["objects", "patent", "trademark", "evidence", "goal"]
    assert AnswerOption.objects.filter(question__scenario=scenario).count() == 22


def test_before_answering_only_always_visible_questions_are_shown(run):
    assert codes(run) == ["objects", "goal"]


@pytest.mark.parametrize("objects, expected", [
    (["jewelry"], ["objects", "patent", "goal"]),
    (["design"], ["objects", "evidence", "goal"]),
    (["photos"], ["objects", "evidence", "goal"]),
    (["name"], ["objects", "trademark", "goal"]),
    (["logo"], ["objects", "trademark", "goal"]),
    (["jewelry", "name"], ["objects", "patent", "trademark", "goal"]),
    (["jewelry", "design", "logo"], ["objects", "patent", "trademark", "evidence", "goal"]),
])
def test_questions_shown_depend_on_objects(run, objects, expected):
    submit_answer(run, "objects", options=objects)
    assert codes(run) == expected


def test_flow_follows_question_order(run):
    submit_answer(run, "objects", options=["jewelry", "design"])
    for code, options in [("patent", ["yes"]), ("evidence", ["file"]), ("goal", ["stop"])]:
        assert get_next_question(run).code == code
        submit_answer(run, code, options=options)
    assert get_next_question(run) is None
    run.refresh_from_db()
    assert run.status == SurveyRun.Status.COMPLETED


def test_no_evidence_option_excludes_the_others(run):
    submit_answer(run, "objects", options=["design"])
    with pytest.raises(AnswerError):
        submit_answer(run, "evidence", options=["none", "file"])
    submit_answer(run, "evidence", options=["file", "messages"])


def test_changing_objects_removes_answers_to_hidden_questions(run):
    submit_answer(run, "objects", options=["jewelry"])
    submit_answer(run, "patent", options=["yes"])
    submit_answer(run, "objects", options=["design"])
    assert not RunAnswer.objects.filter(run=run, question__code="patent").exists()
    assert get_next_question(run).code == "evidence"


def test_reseed_does_not_duplicate(run):
    call_command("seed_surveys")
    assert Question.objects.filter(scenario__slug=SLUG).count() == 5

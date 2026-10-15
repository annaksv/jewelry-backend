import pytest

from apps.surveys.models import AnswerOption, Question, RunAnswer, Scenario, SurveyRun
from apps.surveys.services.engine import build_context, get_next_question, get_progress


@pytest.fixture
def scenario(db):
    sc = Scenario.objects.create(slug="demo", title="Демо")
    q1 = Question.objects.create(scenario=sc, code="q1", order=1, text="Кто вы?")
    for i, (code, tags) in enumerate([("ip", ["org:ip"]), ("llc", ["org:llc"]), ("none", [])], start=1):
        AnswerOption.objects.create(question=q1, code=code, label=code, order=i, tags=tags)
    q2 = Question.objects.create(scenario=sc, code="q2", order=2, text="Только для ИП", show_if={"option": "q1.ip"})
    AnswerOption.objects.create(question=q2, code="a", label="A", order=1)
    q3 = Question.objects.create(scenario=sc, code="q3", order=3, text="Для всех")
    AnswerOption.objects.create(question=q3, code="a", label="A", order=1)
    return sc


@pytest.fixture
def run(scenario):
    return SurveyRun.objects.create(scenario=scenario)


def answer(run, question_code, *option_codes):
    question = Question.objects.get(scenario=run.scenario, code=question_code)
    for code in option_codes:
        RunAnswer.objects.create(run=run, question=question, option=question.options.get(code=code))


def test_first_question_is_q1(run):
    assert get_next_question(run).code == "q1"


def test_branch_shown_after_ip(run):
    answer(run, "q1", "ip")
    assert get_next_question(run).code == "q2"


def test_branch_skipped_for_other_answer(run):
    answer(run, "q1", "llc")
    assert get_next_question(run).code == "q3"


def test_finished_returns_none(run):
    answer(run, "q1", "ip")
    answer(run, "q2", "a")
    answer(run, "q3", "a")
    assert get_next_question(run) is None


def test_context_collects_options_and_tags(run):
    answer(run, "q1", "ip", "llc")
    ctx = build_context(run)
    assert ctx.options == {"q1.ip", "q1.llc"}
    assert ctx.tags == {"org:ip", "org:llc"}
    assert ctx.answered == {"q1"}


def test_progress_changes_with_branching(run):
    assert get_progress(run) == {"current": 1, "total": 2}   # q2 пока скрыт
    answer(run, "q1", "ip")
    assert get_progress(run) == {"current": 2, "total": 3}   # q2 появился

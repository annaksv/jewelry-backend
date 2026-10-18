import pytest
from django.core.management import call_command

from apps.surveys.models import AnswerOption, Question, RunAnswer, Scenario, SurveyRun
from apps.surveys.services.answers import AnswerError, submit_answer
from apps.surveys.services.engine import get_next_question, visible_questions

SLUG = "design-to-sale"
ALL_READY = {f"s{i}": "ready" for i in range(1, 10)}


@pytest.fixture
def run(db):
    call_command("seed_surveys")
    return SurveyRun.objects.create(scenario=Scenario.objects.get(slug=SLUG))


def walk(run, steps):
    """Для каждого шага проверяет, что именно этот вопрос следующий, и отвечает на него."""
    for code, options in steps:
        assert get_next_question(run).code == code
        submit_answer(run, code, options=options)


def test_seed_loads_design_scenario(run):
    scenario = run.scenario
    assert scenario.is_published
    assert scenario.questions.count() == 12
    assert AnswerOption.objects.filter(question__scenario=scenario).count() == 48


def test_only_one_clarifying_block_is_shown(run):
    submit_answer(run, "q1", options=["sell"])
    codes = [q.code for q in visible_questions(run)]
    assert "q2_sell" in codes
    assert [c for c in codes if c.startswith("q2_")] == ["q2_sell"]
    assert len(codes) == 7  # q1, одно уточнение, q3-q7


def test_protect_path_completes_and_last_question_is_optional(run):
    walk(run, [("q1", ["protect"]), ("q2_protect", ["evidence"]), ("q3", ["metal"]),
               ("q4", ["ru_chosen"]), ("q5", ["sample"]), ("q6", ["ip"])])
    assert get_next_question(run).code == "q7"
    submit_answer(run, "q7", skip=True)
    assert get_next_question(run) is None
    run.refresh_from_db()
    assert run.status == SurveyRun.Status.COMPLETED


def test_unknown_path_uses_status_grid(run):
    submit_answer(run, "q1", options=["unknown"])
    assert get_next_question(run).code == "q2_unknown"
    submit_answer(run, "q2_unknown", grid=ALL_READY)
    assert get_next_question(run).code == "q3"
    saved = RunAnswer.objects.filter(run=run, question__code="q2_unknown", value="ready")
    assert saved.count() == 9


def test_status_grid_requires_every_row(run):
    submit_answer(run, "q1", options=["unknown"])
    incomplete = {k: v for k, v in ALL_READY.items() if k != "s9"}
    with pytest.raises(AnswerError):
        submit_answer(run, "q2_unknown", grid=incomplete)


def test_changing_goal_removes_old_clarification(run):
    walk(run, [("q1", ["protect"]), ("q2_protect", ["evidence"])])
    submit_answer(run, "q1", options=["sell"])
    assert not RunAnswer.objects.filter(run=run, question__code="q2_protect").exists()
    assert get_next_question(run).code == "q2_sell"


def test_no_sale_channel_cannot_be_combined_with_others(run):
    with pytest.raises(AnswerError):
        submit_answer(run, "q7", options=["none", "online"])
    submit_answer(run, "q7", options=["online", "store"])


def test_required_question_cannot_be_skipped(run):
    with pytest.raises(AnswerError):
        submit_answer(run, "q3", skip=True)


def test_reseed_does_not_duplicate(run):
    call_command("seed_surveys")
    assert Question.objects.filter(scenario__slug=SLUG).count() == 12

import pytest
from django.db import IntegrityError, transaction

from apps.surveys.models import AnswerOption, Question, RunAnswer, Scenario, SurveyRun


@pytest.fixture
def scenario(db):
    return Scenario.objects.create(slug="open-business", title="Открыть ювелирный бизнес")


@pytest.fixture
def question(scenario):
    return Question.objects.create(scenario=scenario, code="q1", order=1, text="Вы ИП?")


def test_question_code_unique_within_scenario(scenario, question):
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Question.objects.create(scenario=scenario, code="q1", order=2, text="Дубль")


def test_same_question_code_allowed_in_other_scenario(question):
    other = Scenario.objects.create(slug="other", title="Другой")
    Question.objects.create(scenario=other, code="q1", order=1, text="Тоже q1")


def test_option_defaults(question):
    option = AnswerOption.objects.create(question=question, code="yes", label="Да")
    assert option.tags == []
    assert option.is_exclusive is False


def test_option_tags_saved(question):
    option = AnswerOption.objects.create(question=question, code="tm", label="ТЗ", tags=["obj:trademark"])
    option.refresh_from_db()
    assert option.tags == ["obj:trademark"]


def test_run_defaults_to_guest_in_progress(scenario):
    run = SurveyRun.objects.create(scenario=scenario)
    assert run.user is None
    assert run.status == SurveyRun.Status.IN_PROGRESS


def test_same_option_cannot_be_answered_twice(scenario, question):
    option = AnswerOption.objects.create(question=question, code="yes", label="Да")
    run = SurveyRun.objects.create(scenario=scenario)
    RunAnswer.objects.create(run=run, question=question, option=option)
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            RunAnswer.objects.create(run=run, question=question, option=option)

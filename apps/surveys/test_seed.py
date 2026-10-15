import pytest
from django.core.management import call_command

from apps.surveys.models import AnswerOption, Question, Scenario, SurveyRun
from apps.surveys.services.answers import submit_answer
from apps.surveys.services.conditions import AnswerContext, evaluate
from apps.surveys.services.engine import get_next_question


@pytest.fixture
def seeded(db):
    call_command("seed_surveys")


@pytest.fixture
def run(seeded):
    return SurveyRun.objects.create(scenario=Scenario.objects.get(slug="open-business"))


def walk(run, steps):
    """Для каждого шага проверяет, что именно этот вопрос следующий, и отвечает на него."""
    for code, options in steps:
        assert get_next_question(run).code == code
        submit_answer(run, code, options=options)


def test_seed_loads_everything(seeded):
    scenario = Scenario.objects.get(slug="open-business")
    assert scenario.is_published
    assert scenario.questions.count() == 11
    assert AnswerOption.objects.filter(question__scenario=scenario).count() == 40


def test_all_show_if_conditions_are_valid(seeded):
    for question in Question.objects.all():
        evaluate(question.show_if, AnswerContext())  # не должно падать с ConditionError


def test_services_path_skips_production_and_sales(run):
    walk(run, [("q1", ["none"]), ("q2", ["services"]), ("q7", ["new_only"]),
               ("q8", ["own"]), ("q9", ["no"]), ("q10", ["none"])])
    assert get_next_question(run) is None
    run.refresh_from_db()
    assert run.status == SurveyRun.Status.COMPLETED


def test_full_production_and_sales_path(run):
    walk(run, [("q1", ["ip"]), ("q2", ["produce_sell"]), ("q3", ["self"]),
               ("q4", ["metal", "stone"]), ("q5", ["ru"]), ("q6", ["online", "marketplace"]),
               ("q7", ["client"]), ("q7_1", ["repair"]), ("q8", ["both"]),
               ("q9", ["unknown"]), ("q10", ["yes"])])
    assert get_next_question(run) is None


def test_production_only_skips_sales_question(run):
    walk(run, [("q1", ["llc"]), ("q2", ["produce"]), ("q3", ["foreign"]),
               ("q4", ["bijou"]), ("q5", ["abroad"]), ("q7", ["new_only"])])
    assert get_next_question(run).code == "q8"


def test_reseed_does_not_overwrite_edits(seeded):
    question = Question.objects.get(scenario__slug="open-business", code="q1")
    question.text = "Правка юриста"
    question.save()
    call_command("seed_surveys")
    question.refresh_from_db()
    assert question.text == "Правка юриста"
    assert Question.objects.filter(scenario__slug="open-business").count() == 11


def test_reseed_with_overwrite_restores_text(seeded):
    question = Question.objects.get(scenario__slug="open-business", code="q1")
    question.text = "Правка юриста"
    question.save()
    call_command("seed_surveys", overwrite=True)
    question.refresh_from_db()
    assert question.text == "У вас уже есть ИП или юридическое лицо?"

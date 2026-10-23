import pytest
from django.core.management import call_command

from apps.routes.models import ContentBlockLink
from apps.routes.services.builder import get_or_build_route
from apps.surveys.models import AnswerOption, Scenario, SurveyRun
from apps.surveys.services.answers import submit_answer
from apps.surveys.services.conditions import AnswerContext, evaluate

ALL = "/suppliers?from=business"
METALS = "/suppliers?from=business&category=metals"
STONES = "/suppliers?from=business&category=stones"


@pytest.fixture
def seeded(db):
    call_command("seed_surveys")
    call_command("seed_routes")


def steps_for(materials, source="ru"):
    run = SurveyRun.objects.create(scenario=Scenario.objects.get(slug="open-business"))
    answers = [("q1", ["ip"]), ("q2", ["produce"]), ("q3", ["self"]), ("q4", materials), ("q5", [source]),
               ("q7", ["new_only"]), ("q8", ["own"]), ("q9", ["no"]), ("q10", ["yes"])]
    for code, options in answers:
        submit_answer(run, code, options=options)
    return get_or_build_route(run).snapshot["steps"]


def catalog_targets(steps, number):
    return [link["target"] for step in steps if step["number"] == number
            for link in step["links"] if link["kind"] == "catalog"]


@pytest.mark.parametrize("materials, expected", [
    (["metal"], METALS),
    (["stone"], STONES),
    (["metal", "stone"], ALL),
    (["metal_stone"], ALL),
    (["bijou"], ALL),
])
def test_supplier_link_in_step_5_depends_on_materials(seeded, materials, expected):
    assert catalog_targets(steps_for(materials), "5") == [expected]


def test_supplier_link_in_step_4_depends_on_materials(seeded):
    assert catalog_targets(steps_for(["metal"]), "4") == [METALS]
    assert catalog_targets(steps_for(["stone"]), "4") == [STONES]
    assert catalog_targets(steps_for(["metal", "stone"]), "4") == [ALL]
    assert catalog_targets(steps_for(["metal_stone"]), "4") == [ALL]
    assert catalog_targets(steps_for(["bijou"]), "4") == []


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


def test_all_links_are_ready_paths_and_conditions_are_valid(seeded):
    options = AnswerOption.objects.select_related("question")
    valid_options = {f"{o.question.code}.{o.code}" for o in options}
    valid_tags = {tag for o in options for tag in o.tags}
    links = ContentBlockLink.objects.all()
    assert links.count() == 80
    for link in links:
        assert link.kind in {"article", "tool", "catalog", "scenario"}, link.target
        assert link.target.startswith("/"), link.target
        if link.condition:
            evaluate(link.condition, AnswerContext())  # не должно падать
            assert set(_leaves(link.condition, "option")) <= valid_options, link.target
            assert set(_leaves(link.condition, "tag")) <= valid_tags, link.target


def test_reseed_with_overwrite_does_not_duplicate_links(seeded):
    call_command("seed_routes", "--overwrite")
    assert ContentBlockLink.objects.count() == 80

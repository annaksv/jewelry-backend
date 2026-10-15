import pytest

from apps.surveys.services.conditions import AnswerContext, ConditionError, evaluate


@pytest.fixture
def ctx():
    return AnswerContext(
        options={"q2.produce", "q2.sell"},
        tags={"obj:trademark", "reg:tm_no"},
        answered={"q1", "q2"},
        values={"grid.row3": "not_ready"},
    )


def test_empty_condition_is_always_true(ctx):
    assert evaluate({}, ctx) is True
    assert evaluate(None, ctx) is True


def test_option(ctx):
    assert evaluate({"option": "q2.produce"}, ctx) is True
    assert evaluate({"option": "q2.services"}, ctx) is False


def test_tag(ctx):
    assert evaluate({"tag": "obj:trademark"}, ctx) is True
    assert evaluate({"tag": "obj:copyright"}, ctx) is False


def test_answered(ctx):
    assert evaluate({"answered": "q1"}, ctx) is True
    assert evaluate({"answered": "q9"}, ctx) is False


def test_all(ctx):
    assert evaluate({"all": [{"option": "q2.produce"}, {"tag": "obj:trademark"}]}, ctx) is True
    assert evaluate({"all": [{"option": "q2.produce"}, {"tag": "obj:copyright"}]}, ctx) is False


def test_any(ctx):
    assert evaluate({"any": [{"option": "q2.services"}, {"tag": "obj:trademark"}]}, ctx) is True
    assert evaluate({"any": [{"option": "q2.services"}, {"tag": "obj:copyright"}]}, ctx) is False


def test_not(ctx):
    assert evaluate({"not": {"option": "q2.services"}}, ctx) is True
    assert evaluate({"not": {"option": "q2.produce"}}, ctx) is False


def test_nested(ctx):
    cond = {"all": [{"answered": "q1"}, {"any": [{"option": "q2.services"}, {"not": {"tag": "obj:copyright"}}]}]}
    assert evaluate(cond, ctx) is True


def test_value_in(ctx):
    assert evaluate({"value": {"option": "grid.row3", "in": ["not_ready", "unknown"]}}, ctx) is True
    assert evaluate({"value": {"option": "grid.row3", "in": ["ready"]}}, ctx) is False
    assert evaluate({"value": {"option": "grid.row9", "in": ["ready"]}}, ctx) is False


def test_empty_all_and_any(ctx):
    assert evaluate({"all": []}, ctx) is True
    assert evaluate({"any": []}, ctx) is False


def test_unknown_key_raises(ctx):
    with pytest.raises(ConditionError):
        evaluate({"optoin": "q2.produce"}, ctx)


def test_two_keys_raise(ctx):
    with pytest.raises(ConditionError):
        evaluate({"option": "q2.produce", "tag": "x"}, ctx)


def test_value_bad_format_raises(ctx):
    with pytest.raises(ConditionError):
        evaluate({"value": "grid.row3"}, ctx)

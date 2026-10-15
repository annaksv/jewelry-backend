"""Язык условий: {"all": [...]}, {"any": [...]}, {"not": {...}} и листья
option / tag / answered / value. Описание: docs/03-database.md, раздел 1."""

from dataclasses import dataclass, field


class ConditionError(ValueError):
    """Условие записано неправильно (опечатка в админке и т. п.)."""


@dataclass
class AnswerContext:
    """Снимок ответов пользователя, по которому проверяются условия."""

    options: set = field(default_factory=set)    # {"q2.produce", ...}
    tags: set = field(default_factory=set)       # {"obj:trademark", ...}
    answered: set = field(default_factory=set)   # коды вопросов с ответом
    values: dict = field(default_factory=dict)   # {"grid.row3": "ready"}
    skipped: set = field(default_factory=set)    # пропущенные необязательные вопросы


def _as_list(key, arg):
    if not isinstance(arg, list):
        raise ConditionError(f"Для «{key}» нужен список условий")
    return arg


def evaluate(condition, ctx):
    """Возвращает True или False. Пустое условие {} всегда верно."""
    if condition is None or condition == {}:
        return True
    if not isinstance(condition, dict):
        raise ConditionError(f"Условие должно быть объектом, получено: {condition!r}")
    if len(condition) != 1:
        raise ConditionError(f"В условии должен быть ровно один ключ, получено: {list(condition)}")

    (key, arg), = condition.items()

    if key == "all":
        return all(evaluate(c, ctx) for c in _as_list(key, arg))
    if key == "any":
        return any(evaluate(c, ctx) for c in _as_list(key, arg))
    if key == "not":
        return not evaluate(arg, ctx)
    if key == "option":
        return arg in ctx.options
    if key == "tag":
        return arg in ctx.tags
    if key == "answered":
        return arg in ctx.answered
    if key == "value":
        if not isinstance(arg, dict) or "option" not in arg or "in" not in arg:
            raise ConditionError('Для «value» нужен вид {"option": "...", "in": [...]}')
        return ctx.values.get(arg["option"]) in arg["in"]

    raise ConditionError(f"Неизвестное условие: {key!r}")

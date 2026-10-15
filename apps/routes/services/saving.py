"""Привязка прохождения и маршрута к аккаунту."""

from django.db import transaction

from apps.routes.models import Route
from apps.surveys.models import SurveyRun

from .builder import get_or_build_route


@transaction.atomic
def claim_run(run, user):
    """Делает user владельцем прохождения. Возвращает маршрут, если опрос уже завершён, иначе None."""
    run.user = user
    run.anon_token_hash = ""  # гостевой токен после привязки больше не действует
    run.save(update_fields=["user", "anon_token_hash"])  # updated_at не меняем, снимок остаётся прежним
    Route.objects.filter(run=run).update(user=user)
    if run.status == SurveyRun.Status.COMPLETED:
        return get_or_build_route(run)
    return None

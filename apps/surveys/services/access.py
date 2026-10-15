"""Кто может смотреть и менять прохождение."""

import hashlib
import hmac

from rest_framework.exceptions import NotFound

from apps.surveys.models import SurveyRun


def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()


def get_run_for_request(request, run_id):
    """Прохождение доступно владельцу-пользователю или гостю с верным X-Run-Token.
    Во всех остальных случаях отвечаем 404, чтобы не раскрывать, что оно существует."""
    run = SurveyRun.objects.select_related("scenario").filter(pk=run_id).first()
    if run is not None:
        user = request.user
        if user.is_authenticated and run.user_id == user.id:
            return run
        token = request.headers.get("X-Run-Token", "")
        if token and run.user_id is None and run.anon_token_hash:
            if hmac.compare_digest(hash_token(token), run.anon_token_hash):
                return run
    raise NotFound("Прохождение не найдено")

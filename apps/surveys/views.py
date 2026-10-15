import secrets

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Scenario, SurveyRun
from .serializers import (
    AnswerInputSerializer,
    RunCreateSerializer,
    RunStateSerializer,
    ScenarioSerializer,
)
from .services.access import get_run_for_request, hash_token
from .services.answers import AnswerError, submit_answer
from .services.state import build_state

RUN_TOKEN_PARAM = OpenApiParameter(
    name="X-Run-Token", type=str, location=OpenApiParameter.HEADER, required=False,
    description="Токен гостя, выданный при старте прохождения (если пользователь не вошёл)",
)


class ScenarioListView(generics.ListAPIView):
    """Опубликованные сценарии для карточек на главной."""

    queryset = Scenario.objects.filter(is_published=True)
    serializer_class = ScenarioSerializer
    pagination_class = None


class ScenarioDetailView(generics.RetrieveAPIView):
    """Данные страницы входа в сценарий."""

    queryset = Scenario.objects.filter(is_published=True)
    serializer_class = ScenarioSerializer
    lookup_field = "slug"


class RunCreateView(APIView):
    @extend_schema(request=RunCreateSerializer, responses={201: RunStateSerializer})
    def post(self, request):
        """Начать прохождение. Гость получает anon_token (показывается один раз)."""
        serializer = RunCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        scenario = Scenario.objects.filter(slug=serializer.validated_data["scenario"], is_published=True).first()
        if scenario is None:
            raise NotFound("Сценарий не найден")

        run = SurveyRun(scenario=scenario)
        token = None
        if request.user.is_authenticated:
            run.user = request.user
        else:
            token = secrets.token_urlsafe(32)
            run.anon_token_hash = hash_token(token)
        run.save()

        data = build_state(run)
        if token:
            data["anon_token"] = token
        return Response(RunStateSerializer(data).data, status=status.HTTP_201_CREATED)


class RunDetailView(APIView):
    @extend_schema(
        parameters=[
            RUN_TOKEN_PARAM,
            OpenApiParameter("question", str, OpenApiParameter.QUERY, required=False,
                             description="Код вопроса, чтобы показать его (кнопка «Назад»)"),
        ],
        responses=RunStateSerializer,
    )
    def get(self, request, run_id):
        """Текущее состояние: вопрос, прогресс, история."""
        run = get_run_for_request(request, run_id)
        try:
            data = build_state(run, request.query_params.get("question"))
        except LookupError as exc:
            raise NotFound(str(exc))
        return Response(RunStateSerializer(data).data)


class RunAnswerView(APIView):
    @extend_schema(parameters=[RUN_TOKEN_PARAM], request=AnswerInputSerializer, responses=RunStateSerializer)
    def post(self, request, run_id):
        """Отправить ответ (или пропустить вопрос). В ответе: следующий вопрос."""
        run = get_run_for_request(request, run_id)
        serializer = AnswerInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            submit_answer(run, **serializer.validated_data)
        except AnswerError as exc:
            raise ValidationError({"detail": exc.message})
        return Response(RunStateSerializer(build_state(run)).data)

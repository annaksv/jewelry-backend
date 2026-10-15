from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.surveys.services.access import get_run_for_request
from apps.surveys.views import RUN_TOKEN_PARAM

from .models import Route
from .serializers import ClaimResultSerializer, RouteSerializer, SavedRouteSerializer
from .services.builder import RunNotCompleted, get_or_build_route, route_payload
from .services.saving import claim_run


class RunRouteView(APIView):
    @extend_schema(parameters=[RUN_TOKEN_PARAM], responses={200: RouteSerializer})
    def get(self, request, run_id):
        """Готовый маршрут по завершённому прохождению. 409, если опрос ещё не пройден до конца."""
        run = get_run_for_request(request, run_id)
        try:
            route = get_or_build_route(run)
        except RunNotCompleted as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)
        return Response(RouteSerializer(route_payload(route)).data)


class RunClaimView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[RUN_TOKEN_PARAM], request=None, responses={200: ClaimResultSerializer})
    def post(self, request, run_id):
        """Сохранить прохождение и маршрут в личном кабинете. Нужен вход; гость передаёт X-Run-Token."""
        run = get_run_for_request(request, run_id)
        route = claim_run(run, request.user)
        data = {"run_id": run.id, "status": run.status, "route_id": route.id if route else None, "is_saved": True}
        return Response(ClaimResultSerializer(data).data)


class MyRoutesView(generics.ListAPIView):
    """Сохранённые маршруты текущего пользователя (новые первыми)."""

    permission_classes = [IsAuthenticated]
    serializer_class = SavedRouteSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Route.objects.none()
        return Route.objects.filter(user=self.request.user).select_related("scenario")


class SavedRouteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: RouteSerializer})
    def get(self, request, route_id):
        """Сохранённый маршрут целиком. Чужие маршруты недоступны (404)."""
        route = Route.objects.select_related("scenario").filter(pk=route_id, user=request.user).first()
        if route is None:
            raise NotFound("Маршрут не найден")
        return Response(RouteSerializer(route_payload(route)).data)

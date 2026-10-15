from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.surveys.services.access import get_run_for_request
from apps.surveys.views import RUN_TOKEN_PARAM

from .serializers import RouteSerializer
from .services.builder import RunNotCompleted, get_or_build_route, route_payload


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

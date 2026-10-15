from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Route


class RouteLinkSerializer(serializers.Serializer):
    label = serializers.CharField()
    kind = serializers.CharField(help_text="article, tool, catalog или external")
    target = serializers.CharField(allow_blank=True, help_text="slug статьи, код инструмента, вкладка каталога или URL")


class RouteStepSerializer(serializers.Serializer):
    number = serializers.CharField(allow_blank=True, help_text="Номер шага: «1», «7.1»")
    title = serializers.CharField()
    body = serializers.CharField(allow_blank=True)
    links = RouteLinkSerializer(many=True)


class RouteSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    run_id = serializers.UUIDField(help_text="Прохождение, из которого собран маршрут (для «Изменить ответы»)")
    scenario = serializers.CharField()
    scenario_title = serializers.CharField()
    schema_version = serializers.IntegerField()
    is_saved = serializers.BooleanField(help_text="true, если маршрут привязан к аккаунту")
    steps = RouteStepSerializer(many=True)


class ClaimResultSerializer(serializers.Serializer):
    run_id = serializers.UUIDField()
    status = serializers.CharField(help_text="in_progress или completed")
    route_id = serializers.UUIDField(allow_null=True, help_text="null, если опрос ещё не завершён")
    is_saved = serializers.BooleanField()


class SavedRouteSerializer(serializers.ModelSerializer):
    run_id = serializers.UUIDField(read_only=True)
    scenario = serializers.CharField(source="scenario.slug")
    scenario_title = serializers.CharField(source="scenario.title")
    steps_count = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ["id", "run_id", "scenario", "scenario_title", "steps_count", "created_at", "updated_at"]

    @extend_schema_field(serializers.IntegerField())
    def get_steps_count(self, obj):
        return len(obj.snapshot.get("steps", []))

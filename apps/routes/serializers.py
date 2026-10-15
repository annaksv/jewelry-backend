from rest_framework import serializers


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
    scenario = serializers.CharField()
    scenario_title = serializers.CharField()
    schema_version = serializers.IntegerField()
    is_saved = serializers.BooleanField(help_text="true, если маршрут привязан к аккаунту")
    steps = RouteStepSerializer(many=True)

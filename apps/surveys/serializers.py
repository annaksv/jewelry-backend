from rest_framework import serializers

from .models import Scenario


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = ["slug", "title", "description", "card_title", "card_subtitle"]


class RunCreateSerializer(serializers.Serializer):
    scenario = serializers.CharField(help_text="slug сценария, например open-business")


class AnswerInputSerializer(serializers.Serializer):
    question = serializers.CharField(help_text="Код вопроса, например q1")
    options = serializers.ListField(
        child=serializers.CharField(), required=False,
        help_text="Коды выбранных вариантов (для вопросов «один вариант» и «несколько»)",
    )
    grid = serializers.DictField(
        child=serializers.CharField(), required=False,
        help_text='Для таблицы статусов: {"код строки": "ready" | "not_ready" | "unknown"}',
    )
    skip = serializers.BooleanField(required=False, default=False, help_text="Пропустить необязательный вопрос")


class OptionSerializer(serializers.Serializer):
    code = serializers.CharField()
    label = serializers.CharField()
    is_exclusive = serializers.BooleanField()


class QuestionStateSerializer(serializers.Serializer):
    code = serializers.CharField()
    step_label = serializers.CharField(allow_blank=True)
    section_label = serializers.CharField(allow_blank=True)
    text = serializers.CharField()
    help_text = serializers.CharField(allow_blank=True)
    kind = serializers.CharField(help_text="single, multi или status_grid")
    is_required = serializers.BooleanField()
    options = OptionSerializer(many=True)
    selected = serializers.ListField(child=serializers.CharField(), help_text="Уже выбранные варианты")
    grid_values = serializers.DictField(child=serializers.CharField(), help_text="Статусы строк таблицы")
    is_skipped = serializers.BooleanField()


class ProgressSerializer(serializers.Serializer):
    current = serializers.IntegerField()
    total = serializers.IntegerField()


class RunStateSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    scenario = serializers.CharField()
    status = serializers.CharField(help_text="in_progress или completed")
    question = QuestionStateSerializer(allow_null=True, help_text="null, если вопросов больше нет")
    progress = ProgressSerializer()
    history = serializers.ListField(child=serializers.CharField(), help_text="Коды уже пройденных вопросов по порядку")
    anon_token = serializers.CharField(required=False, help_text="Только при старте у гостя; показывается один раз")

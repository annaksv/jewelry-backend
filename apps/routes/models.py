import uuid

from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel
from apps.surveys.models import Question, Scenario, SurveyRun


class ContentBlock(TimeStampedModel):
    """Кусок текста маршрута («шаг»)."""

    class Role(models.TextChoices):
        STEP = "step", "Шаг маршрута"
        RESULT_SCREEN = "result_screen", "Экран результата"
        PROTECTION_METHOD = "protection_method", "Способ защиты"
        STAGE_CARD = "stage_card", "Карточка этапа"
        GENERAL = "general", "Общий блок"

    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="blocks", verbose_name="Сценарий")
    code = models.CharField("Код блока", max_length=100, unique=True, help_text="Например: biz.q1.ip")
    role = models.CharField("Роль", max_length=30, choices=Role.choices, default=Role.STEP)
    title = models.CharField("Заголовок", max_length=200)
    body = models.TextField("Текст", blank=True, help_text="Текст, который увидит пользователь")
    dedupe_key = models.CharField("Ключ уникальности", max_length=100, blank=True,
                                  help_text="Блоки с одинаковым ключом не выводятся дважды")

    class Meta:
        ordering = ["scenario", "code"]
        verbose_name = "Блок маршрута"
        verbose_name_plural = "Блоки маршрута"

    def __str__(self):
        return f"{self.code}: {self.title}"


class ContentBlockLink(TimeStampedModel):
    """Ссылка внутри блока (кнопка после текста)."""

    class Kind(models.TextChoices):
        ARTICLE = "article", "Статья"
        TOOL = "tool", "Инструмент сайта"
        CATALOG = "catalog", "Каталог поставщиков"
        EXTERNAL = "external", "Внешний сайт"

    block = models.ForeignKey(ContentBlock, on_delete=models.CASCADE, related_name="links", verbose_name="Блок")
    order = models.PositiveIntegerField("Порядок", default=0)
    label = models.CharField("Текст ссылки", max_length=200)
    kind = models.CharField("Тип", max_length=20, choices=Kind.choices)
    target = models.CharField("Цель", max_length=300, blank=True,
                              help_text="Статья: её код (slug). Инструмент: okved-check. "
                                        "Каталог: metals, stones или all. Внешний сайт: адрес.")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Ссылка блока"
        verbose_name_plural = "Ссылки блока"

    def __str__(self):
        return self.label


class RouteRule(TimeStampedModel):
    """Когда блок попадает в маршрут."""

    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="route_rules",
                                 verbose_name="Сценарий")
    block = models.ForeignKey(ContentBlock, on_delete=models.PROTECT, related_name="rules", verbose_name="Блок")
    condition = models.JSONField("Условие", default=dict, blank=True, help_text="Пусто ({}) = всегда")
    position = models.PositiveIntegerField("Позиция", default=0, help_text="Порядок блоков в маршруте")
    step_question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.SET_NULL, related_name="+",
                                      verbose_name="Вопрос для номера шага")
    promote_if = models.JSONField("Поднять наверх, если", null=True, blank=True,
                                  help_text="Если условие верно, блок идёт первым")

    class Meta:
        ordering = ["scenario", "position", "id"]
        verbose_name = "Правило маршрута"
        verbose_name_plural = "Правила маршрута"

    def __str__(self):
        return f"{self.position}: {self.block.code}"


class Route(TimeStampedModel):
    """Готовый маршрут пользователя (снимок на момент сборки)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    run = models.OneToOneField(SurveyRun, on_delete=models.CASCADE, related_name="route", verbose_name="Прохождение")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
                             related_name="routes", verbose_name="Пользователь")
    scenario = models.ForeignKey(Scenario, on_delete=models.PROTECT, related_name="routes", verbose_name="Сценарий")
    result_code = models.CharField("Код результата", max_length=100, blank=True)
    snapshot = models.JSONField("Снимок маршрута", default=dict)
    schema_version = models.PositiveIntegerField("Версия формата", default=1)
    source_updated_at = models.DateTimeField("Версия прохождения, по которой собран", null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"

    def __str__(self):
        return f"{self.scenario.slug} / {self.id}"

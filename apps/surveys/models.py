import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.db import models

from apps.common.models import TimeStampedModel


class Scenario(TimeStampedModel):
    """Сценарий: «Открыть ювелирный бизнес», «Нарушение прав», «Дизайн»."""

    slug = models.SlugField("Код (slug)", unique=True, help_text="Например: open-business")
    title = models.CharField("Заголовок", max_length=200)
    description = models.TextField("Описание страницы входа", blank=True)
    card_title = models.CharField("Заголовок карточки на главной", max_length=200, blank=True)
    card_subtitle = models.CharField("Подзаголовок карточки", max_length=300, blank=True)
    order = models.PositiveIntegerField("Порядок на главной", default=0)
    is_published = models.BooleanField("Опубликован", default=False)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Сценарий"
        verbose_name_plural = "Сценарии"

    def __str__(self):
        return self.title


class Question(TimeStampedModel):
    """Вопрос сценария."""

    class Kind(models.TextChoices):
        SINGLE = "single", "Один вариант"
        MULTI = "multi", "Несколько вариантов"
        STATUS_GRID = "status_grid", "Таблица статусов"

    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="questions", verbose_name="Сценарий")
    code = models.CharField("Код вопроса", max_length=50, help_text="Например: q2, q7_1")
    step_label = models.CharField("Номер шага", max_length=20, blank=True, help_text="Например: 1, 7.1, 2А")
    section_label = models.CharField("Подпись раздела", max_length=100, blank=True, help_text="Например: ВАШ БИЗНЕС")
    order = models.PositiveIntegerField("Порядок показа", default=0)
    text = models.TextField("Формулировка")
    help_text = models.CharField("Подсказка", max_length=300, blank=True)
    kind = models.CharField("Тип", max_length=20, choices=Kind.choices, default=Kind.SINGLE)
    is_required = models.BooleanField("Обязательный", default=True)
    show_if = models.JSONField("Условие показа", default=dict, blank=True, help_text="Пусто ({}) = показывать всегда")

    class Meta:
        ordering = ["scenario", "order", "id"]
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        constraints = [
            models.UniqueConstraint(fields=["scenario", "code"], name="uniq_question_code_per_scenario"),
        ]

    def __str__(self):
        return f"{self.scenario.slug}: {self.code}"


class AnswerOption(TimeStampedModel):
    """Вариант ответа (для status_grid это строка таблицы)."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options", verbose_name="Вопрос")
    code = models.CharField("Код варианта", max_length=50)
    label = models.CharField("Текст", max_length=300)
    order = models.PositiveIntegerField("Порядок", default=0)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True, verbose_name="Теги",
                      help_text="Через запятую, например: obj:trademark")
    is_exclusive = models.BooleanField("Исключающий", default=False,
                                       help_text="Если выбран, снимает остальные варианты")

    class Meta:
        ordering = ["question", "order", "id"]
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"
        constraints = [
            models.UniqueConstraint(fields=["question", "code"], name="uniq_option_code_per_question"),
        ]
        indexes = [GinIndex(fields=["tags"], name="answeroption_tags_gin")]

    def __str__(self):
        return f"{self.question.code}.{self.code}"


class SurveyRun(TimeStampedModel):
    """Одно прохождение опроса. У гостя user пустой."""

    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "В процессе"
        COMPLETED = "completed", "Завершено"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scenario = models.ForeignKey(Scenario, on_delete=models.PROTECT, related_name="runs", verbose_name="Сценарий")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
                             related_name="survey_runs", verbose_name="Пользователь")
    anon_token_hash = models.CharField("Хэш токена гостя", max_length=64, blank=True, db_index=True)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)
    completed_at = models.DateTimeField("Завершено", null=True, blank=True)
    skipped_questions = models.JSONField("Пропущенные вопросы", default=list, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Прохождение"
        verbose_name_plural = "Прохождения"

    def __str__(self):
        return f"{self.scenario.slug} / {self.id}"


class RunAnswer(TimeStampedModel):
    """Один выбранный вариант в прохождении."""

    class GridValue(models.TextChoices):
        READY = "ready", "Готово"
        NOT_READY = "not_ready", "Не готово"
        UNKNOWN = "unknown", "Не знаю"

    run = models.ForeignKey(SurveyRun, on_delete=models.CASCADE, related_name="answers", verbose_name="Прохождение")
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name="+", verbose_name="Вопрос")
    option = models.ForeignKey(AnswerOption, on_delete=models.PROTECT, related_name="+", verbose_name="Вариант")
    value = models.CharField("Значение (для таблицы)", max_length=20, choices=GridValue.choices, blank=True)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        constraints = [
            models.UniqueConstraint(fields=["run", "option"], name="uniq_answer_option_per_run"),
        ]

    def __str__(self):
        return f"{self.run_id}: {self.option}"

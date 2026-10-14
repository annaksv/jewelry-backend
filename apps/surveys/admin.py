from django.contrib import admin

from .models import AnswerOption, Question, RunAnswer, Scenario, SurveyRun


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 1


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "order", "is_published")
    list_editable = ("order", "is_published")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("scenario", "order", "step_label", "code", "text", "kind")
    list_filter = ("scenario", "kind")
    search_fields = ("code", "text")
    ordering = ("scenario", "order")
    inlines = [AnswerOptionInline]


class RunAnswerInline(admin.TabularInline):
    model = RunAnswer
    extra = 0
    can_delete = False
    readonly_fields = ("question", "option", "value")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(SurveyRun)
class SurveyRunAdmin(admin.ModelAdmin):
    list_display = ("id", "scenario", "user", "status", "created_at")
    list_filter = ("scenario", "status")
    readonly_fields = ("id", "anon_token_hash", "completed_at")
    inlines = [RunAnswerInline]

from django.contrib import admin

from .models import ContentBlock, ContentBlockLink, Route, RouteRule


class ContentBlockLinkInline(admin.TabularInline):
    model = ContentBlockLink
    extra = 1


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "scenario", "role")
    list_filter = ("scenario", "role")
    search_fields = ("code", "title", "body")
    inlines = [ContentBlockLinkInline]


@admin.register(RouteRule)
class RouteRuleAdmin(admin.ModelAdmin):
    list_display = ("position", "block", "scenario", "step_question")
    list_filter = ("scenario",)
    ordering = ("scenario", "position")


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("id", "scenario", "user", "updated_at")
    list_filter = ("scenario",)
    readonly_fields = ("id", "run", "user", "scenario", "result_code", "snapshot", "schema_version",
                       "source_updated_at")

    def has_add_permission(self, request):
        return False

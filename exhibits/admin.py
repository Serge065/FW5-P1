from django.contrib import admin
from .models import Exhibit, Condition


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "label",
        "needs_restoration",
        "needs_check",
    )
    search_fields = ("code", "label")
    list_filter = ("needs_restoration", "needs_check")


@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "author",
        "collection",
        "year",
        "price",
        "condition",
        "is_available",
    )

    list_display_links = ("id", "name")

    search_fields = (
        "name",
        "author__name",
        "author__lastname",
        "collection__name",
    )

    list_filter = (
        "condition",
        "collection",
        "is_available",
        "year",
    )

    ordering = ("-year", "name")
    list_per_page = 20
    list_select_related = ("author", "collection", "condition")
    view_on_site = True
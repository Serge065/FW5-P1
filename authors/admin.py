from django.contrib import admin
from .models import Author
from exhibits.models import Exhibit


class ExhibitInline(admin.TabularInline):
    model = Exhibit
    fields = ("name", "collection", "year", "condition", "is_available")
    extra = 0
    show_change_link = True


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "lastname", "exhibits_count")
    list_display_links = ("id", "name")
    search_fields = ("name", "lastname")
    ordering = ("lastname", "name")
    list_per_page = 20
    inlines = (ExhibitInline,)

    @admin.display(description="Количество экспонатов")
    def exhibits_count(self, obj):
        return obj.exhibits.count()
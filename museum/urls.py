from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("homepage.urls")),
    path("exhibits/", include("exhibits.urls")),
    path("authors/", include("authors.urls")),
    path("collections/", include("colections.urls")),
]

handler404 = "homepage.views.page_not_found"

admin.site.site_header = "Администрирование музейного каталога"
admin.site.site_title = "Музейный каталог"
admin.site.index_title = "Управление данными музея"
from django.urls import path
from . import views

app_name = "authors"

urlpatterns = [
    path("", views.authors, name="list"),
    path("<int:author_id>/", views.author_detail, name="detail"),
]

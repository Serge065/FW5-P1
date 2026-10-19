from django.urls import path
from . import views

app_name = "collections"

urlpatterns = [
    path("", views.collections, name="list"),
    path("<int:collection_id>/", views.collection_detail, name="detail"),
]

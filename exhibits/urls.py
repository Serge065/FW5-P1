from django.urls import path
from . import views

app_name = "exhibits"

urlpatterns = [
    path("", views.exhibits, name="list"),
    path("<int:exhibit_id>/", views.exhibit_detail, name="detail"),
]

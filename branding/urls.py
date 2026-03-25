from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/branding/", views.branding_settings, name="branding_settings"),
]
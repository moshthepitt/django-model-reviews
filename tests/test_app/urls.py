"""URLs for testing."""
from django.urls import path

from model_reviews import views

urlpatterns = [path("review/<int:pk>", views.ReviewView.as_view())]

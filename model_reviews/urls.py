"""urls module."""
from django.urls import path

from model_reviews.views import ReviewView

app_name = "partners"

urlpatterns = [
    path("review/<int:pk>", ReviewView.as_view(), name="perform_review"),
]

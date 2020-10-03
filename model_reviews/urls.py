"""urls module."""
from django.urls import path

from model_reviews.views import BulkReviewsView, ReviewView

app_name = "partners"

urlpatterns = [
    path("review/<int:pk>", ReviewView.as_view(), name="perform_review"),
    path("bulk-review", BulkReviewsView.as_view(), name="perform_bulk_review"),
]

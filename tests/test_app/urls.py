"""URLs for testing."""
from django.http import HttpResponse
from django.urls import path

from model_reviews import views


def homeview(request):
    """Return home page."""
    return HttpResponse("<h1>home page</h1>")


urlpatterns = [
    path("", homeview),
    path("bulk", views.BulkReviewsView.as_view()),
    path("review/<int:pk>", views.ReviewView.as_view()),
]

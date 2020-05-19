"""Side effects module."""
from django.db import models

from model_reviews.constants import USER


def set_review_user(review_obj: models.Model):
    """
    Set user for review model object.

    This is the default strategy of auto-setting the user for a review object.
    It simply sets the user using a field on the model object that is under review.
    """
    if not review_obj.user:
        object_under_review = review_obj.content_object
        review_obj.user = getattr(object_under_review, USER, None)

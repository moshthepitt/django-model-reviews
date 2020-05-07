"""utils module."""
from model_reviews.models import ModelReview


def process_review(instance: ModelReview):
    """Process a review."""
    reviewed_obj = instance.content_object
    reviewed_obj.review_status = instance.review_status
    reviewed_obj.review_date = instance.review_date
    reviewed_obj.review_reason = instance.review_reason
    reviewed_obj.review_comments = instance.review_comments
    reviewed_obj.save()

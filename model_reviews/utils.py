"""utils module."""
from django.db.models import Max

from model_reviews.models import ModelReview, Reviewer


def process_review(instance: ModelReview):
    """Process a review."""
    reviewed_obj = instance.content_object
    reviewed_obj.review_status = instance.review_status
    reviewed_obj.review_date = instance.review_date
    reviewed_obj.save()
    # side effects
    reviewed_obj.run_side_effect(review_obj=instance)


def perform_review(review: ModelReview, data: dict):
    """Perform a review."""
    # check if all the reviewers are the same level
    reviewers = Reviewer.objects.filter(review=review)
    if len(list(set(reviewers.values_list("level", flat=True)))) == 1:
        # save review as done
        review.review_status = data["review_status"]
        review.save()
    else:
        # check if at least one of the highest level people has done the review
        max_level = reviewers.aggregate(max_lvl=Max("level"))["max_lvl"]
        highest_lvl = reviewers.filter(reviewed=True, level=max_level).order_by(
            "-review_date", "-level"
        )
        if highest_lvl.exists():
            # save review as done
            review.review_status = data["review_status"]
            review.save()

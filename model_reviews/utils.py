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


def perform_review(review: ModelReview):
    """Perform a review."""
    # check if all the reviewers are the same level
    reviewers = Reviewer.objects.filter(review=review)
    relevant_reviewer = None
    if len(list(set(reviewers.values_list("level", flat=True)))) == 1:
        # get the most recent reviewer
        relevant_reviewer = (
            reviewers.filter(reviewed=True).order_by("-review_date").first()
        )
    else:
        # check if at least one of the highest level people has done the review
        max_level = reviewers.aggregate(max_lvl=Max("level"))["max_lvl"]
        relevant_reviewer = (
            reviewers.filter(reviewed=True, level=max_level)
            .order_by("-review_date", "-level")
            .first()
        )

    if relevant_reviewer:
        # save review as done
        review.review_date = relevant_reviewer.review_date
        review.review_status = relevant_reviewer.review_status
        review.save()

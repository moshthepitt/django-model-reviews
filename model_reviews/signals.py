"""Signals module for model_reviews."""
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver
from django.utils.module_loading import import_string

from model_reviews.models import AbstractReview, ModelReview, Reviewer
from model_reviews.utils import process_review


@receiver(pre_save)
def approvable_before_save(  # pylint: disable=bad-continuation
    sender, instance, **kwargs
):  # pylint: disable=unused-argument
    """
    Perform actions before the approvable item is saved.

    For already created objects:
        1. Get the corresponding ModelReview object
        2. Update the ModelReview object is created sandbox
        3. Revert the changes in the approvable object before saving
    """
    if isinstance(instance, AbstractReview) and not isinstance(instance, ModelReview):
        if instance.pk is not None:  # deal with updated instances only
            obj_type = ContentType.objects.get_for_model(instance)
            try:
                obj_type.get_object_for_this_type(pk=instance.pk)
            except ObjectDoesNotExist:
                pass
            else:
                review, _ = ModelReview.objects.get_or_create(
                    content_type=obj_type, object_id=instance.pk
                )
                diff = review.get_diff(source=instance)

                if review.needs_review():
                    if diff:
                        # only update the sandbox if review is needed and there is a diff
                        review.update_sandbox(source=instance)
                        # only revert the instance if there is a diff
                        instance.revert()


@receiver(post_save)
def approvable_after_save(  # pylint: disable=bad-continuation
    sender, instance, raw, created, **kwargs
):  # pylint: disable=unused-argument
    """
    Perform actions after the approvable item has been saved.

    This is only relevant for new objects, where:
        1. A ModelReview object is created
        2. The sandbox on ModelReview is populated
    """
    if isinstance(instance, AbstractReview) and not isinstance(instance, ModelReview):
        if created:
            obj_type = ContentType.objects.get_for_model(instance)
            review = ModelReview(content_type=obj_type, object_id=instance.pk)
            review.update_sandbox(source=instance, do_save=False)
            review.save()


@receiver(pre_save, sender=ModelReview)
def modelreview_before_save(  # pylint: disable=bad-continuation
    sender, instance, **kwargs
):  # pylint: disable=unused-argument
    """Perform actions before the ModelReview object has been saved."""
    # run set_user_function
    if instance.content_object:
        if instance.content_object.set_user_function:
            set_user_function = import_string(instance.content_object.set_user_function)
            set_user_function(review_obj=instance)


@receiver(post_save, sender=ModelReview)
def modelreview_after_save(  # pylint: disable=bad-continuation
    sender, instance, raw, created, **kwargs
):  # pylint: disable=unused-argument
    """Perform actions after the ModelReview object has been saved."""
    if not instance.needs_review():
        process_review(instance)
        instance.send_review_complete_notification()
    if instance.content_object:
        if instance.content_object.set_reviewers_function:
            set_reviewers_function = import_string(
                instance.content_object.set_reviewers_function
            )
            set_reviewers_function(review_obj=instance)


@receiver(post_save, sender=Reviewer)
def reviewer_after_save(  # pylint: disable=bad-continuation
    sender, instance, raw, created, **kwargs
):  # pylint: disable=unused-argument
    """Perform actions after the Reviewer object has been saved."""
    if created:
        instance.send_request_for_review()

"""Signals module for model_reviews."""
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver

from model_reviews.models import AbstractReview, ModelReview
from model_reviews.utils import process_review


@receiver(pre_save)
def approvable_before_save(  # pylint: disable=bad-continuation
    sender, instance, **kwargs
):  # pylint: disable=unused-argument
    """
    Manage data in the approvable item before it is saved.

    For already created objects, update the sandbox with current object status,
    and then revert the changes in the object before saving.
    """
    if isinstance(instance, AbstractReview) and not isinstance(instance, ModelReview):
        if instance.pk is not None:  # deal with updated instances only
            obj_type = ContentType.objects.get_for_model(instance)
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
    """Manage data in the approvable item after it has been."""
    if isinstance(instance, AbstractReview) and not isinstance(instance, ModelReview):
        if created:
            obj_type = ContentType.objects.get_for_model(instance)
            review = ModelReview(content_type=obj_type, object_id=instance.pk)
            review.update_sandbox(source=instance, do_save=False)
            review.save()


@receiver(post_save, sender=ModelReview)
def modelreview_after_save(  # pylint: disable=bad-continuation
    sender, instance, raw, created, **kwargs
):  # pylint: disable=unused-argument
    """Manage data in the approvable item after it has been."""
    if not instance.needs_review():
        process_review(instance)

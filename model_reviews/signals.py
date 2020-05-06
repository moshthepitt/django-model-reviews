"""Signals module for model_reviews."""
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from model_reviews.models import AbstractReview, ModelReview


@receiver(post_save)
def approvable_after_save(  # pylint: disable=bad-continuation
    sender, instance, raw, created, **kwargs
):  # pylint: disable=unused-argument
    """Manage data in the approvable item after it has been."""
    if isinstance(instance, AbstractReview) and not isinstance(instance, ModelReview):
        if created:
            obj_type = ContentType.objects.get_for_model(instance)
            review = ModelReview(content_type=obj_type, object_id=instance.id)
            review.save()

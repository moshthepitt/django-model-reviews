"""Models module for model reviews."""

from typing import List, Optional

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from model_reviews.constants import SANDBOX_FIELD

USER = settings.AUTH_USER_MODEL


class AbstractReview(models.Model):
    """Model definition for AbstractReview."""

    APPROVED = "1"
    REJECTED = "2"
    PENDING = "3"

    STATUS_CHOICES = (
        (APPROVED, _("Approved")),
        (PENDING, _("Pending")),
        (REJECTED, _("Rejected")),
    )

    # model_review options
    monitored_fields: List[str] = ["review_status", "review_date"]
    side_effection_function: Optional[str] = None
    set_reviewers_function: Optional[str] = None
    set_user_function: Optional[str] = "model_reviews.side_effects.set_review_user"

    # model fields start here

    review_status = models.CharField(
        _("Review Status"),
        max_length=1,
        choices=STATUS_CHOICES,
        default=PENDING,
        blank=True,
        db_index=True,
    )
    review_date = models.DateTimeField(
        _("Review Date"), blank=True, default=None, null=True
    )

    class Meta:
        """Meta definition for AbstractReview."""

        abstract = True

    def revert(self) -> bool:
        """
        Revert the instance to its last saved state.

        This method deletes unsaved changes on source model instance.

        Returns:
            `True` if revert was possible, `False` otherwise.
        """
        model = self._meta.model
        try:
            self.refresh_from_db()
            return True
        except model.DoesNotExist:
            return False

    def run_side_effect(self, review_obj: models.Model = None) -> None:
        """
        Run side effect function.

        This method runs the side effect function defined on the approvable model.
        The side effect is run once after an approval/rejection.
        """
        if self.side_effection_function:
            side_effect = import_string(self.side_effection_function)
            side_effect(review_obj=review_obj)


class ModelReview(AbstractReview):
    """Model definition for ModelReview."""

    user = models.ForeignKey(
        USER,
        related_name="modelreview_user",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        null=True,
        default=None,
        blank=True,
        help_text=_("The user who submitted the request for review"),
    )
    content_type = models.ForeignKey(
        ContentType, verbose_name=_("Content Type"), on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(_("Object ID"), db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)
    data = JSONField(_("Data"), encoder=DjangoJSONEncoder, default=dict, blank=False)
    reviewers = models.ManyToManyField(
        USER,
        related_name="modelreview_reviewers",
        verbose_name=_("Reviewer(s)"),
        through="Reviewer",
        through_fields=("review", "user"),
    )

    class Meta:
        """Meta definition for ModelReview."""

        abstract = False
        verbose_name = _("Model Review")
        verbose_name_plural = _("Model Reviews")
        indexes = [models.Index(fields=["content_type", "object_id"])]

    def __str__(self):
        """Unicode representation of ModelReview."""
        return f"{self.content_object} review"

    def get_diff(self, source: models.Model = None) -> Optional[List[str]]:
        """
        Return the difference between the source data and the data in review model.

        Returns:
            A list of monitored field names that are different in the source.

        """
        source = source or self.content_object
        data = self.data.get(SANDBOX_FIELD, dict())

        source_data = {
            field: getattr(source, field) for field in self._get_monitored_fields()
        }

        return [key for key in data.keys() if data[key] != source_data[key]] or None

    def _get_monitored_fields(self, source: models.Model = None) -> List[str]:
        """Return the list of monitored field names."""
        source = source or self.content_object
        return source.monitored_fields

    def needs_review(self) -> bool:
        """Check if review is needed."""
        return self.review_status == ModelReview.PENDING

    def update_sandbox(self, source: models.Model = None, do_save: bool = True) -> None:
        """Update fields of the sandbox to reflect the state of the source."""
        source = source or self.content_object
        fields = self._get_monitored_fields(source=source)
        values = {key: getattr(source, key) for key in fields if hasattr(source, key)}
        if self.data.get(SANDBOX_FIELD):
            self.data[SANDBOX_FIELD].update(values)
        else:
            self.data[SANDBOX_FIELD] = values
        if do_save:
            self.save()


class Reviewer(models.Model):
    """Model definition for Reviewer."""

    user = models.ForeignKey(USER, verbose_name=_("User"), on_delete=models.CASCADE)
    review = models.ForeignKey(
        "ModelReview", verbose_name=_("Model Review"), on_delete=models.CASCADE
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)
    level = models.IntegerField(
        _("Level"),
        default=0,
        blank=True,
        db_index=True,
        help_text=_(
            "Used to control when a reviewer is asked for their review. "
            "For example, a level 2 reviewer may have to wait until all "
            "level 1 reviews are done."
        ),
    )
    reviewed = models.BooleanField(
        _("Reviewed"), default=False, blank=True, db_index=True
    )
    review_date = models.DateTimeField(
        _("Review Date"), null=True, default=None, blank=True
    )

    class Meta:
        """Meta definition for Reviewer."""

        verbose_name = _("Reviewer")
        verbose_name_plural = _("Reviewers")

    def __str__(self):
        """Unicode representation of Reviewer."""
        return f"{self.user} review for {self.review}"

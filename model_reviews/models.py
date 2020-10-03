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

from model_reviews.constants import (
    EMAIL_TEMPLATE,
    EMAIL_TEMPLATE_PATH,
    REVIEW_COMPLETE_EMAIL_SUBJ,
    REVIEW_COMPLETE_EMAIL_TXT,
    REVIEW_REQUEST_EMAIL_SUBJ,
    REVIEW_REQUEST_EMAIL_TXT,
    SANDBOX_FIELD,
)

USER = settings.AUTH_USER_MODEL


class BaseReview(models.Model):
    """Model definition for BaseReview."""

    APPROVED = "1"
    REJECTED = "2"
    PENDING = "3"

    STATUS_CHOICES = (
        (APPROVED, _("Approved")),
        (PENDING, _("Pending")),
        (REJECTED, _("Rejected")),
    )

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
        """Meta definition for BaseReview."""

        abstract = True


class AbstractReview(BaseReview):
    """Model definition for AbstractReview."""

    # model_review options
    # List of fields that need moderation/review
    monitored_fields: List[str] = ["review_status", "review_date"]
    # path to function that will be run after successful review
    side_effect_function: Optional[str] = None
    # path to function that will be used to determine reviewers
    set_reviewers_function: Optional[str] = None
    # path to function that will be used to determine the user for a review object
    set_user_function: Optional[str] = "model_reviews.side_effects.set_review_user"
    # path to function that will be used to send email to reviewers
    request_for_review_function: Optional[
        str
    ] = "model_reviews.emails.send_single_request_for_review"
    # path to function that will be used to send email to user after review
    review_complete_notify_function: Optional[
        str
    ] = "model_reviews.emails.send_review_complete_notice"
    # path to function that will be used to determine reviewers
    get_next_reviewers_function: Optional[str] = None
    # emails options
    review_request_email_subject = _(REVIEW_REQUEST_EMAIL_SUBJ)
    review_request_email_body = _(REVIEW_REQUEST_EMAIL_TXT)
    review_complete_email_subject = _(REVIEW_COMPLETE_EMAIL_SUBJ)
    review_complete_email_body = _(REVIEW_COMPLETE_EMAIL_TXT)
    email_template = EMAIL_TEMPLATE
    email_template_path = EMAIL_TEMPLATE_PATH

    # model fields
    review_reason = models.TextField(_("Review Reason"), blank=True, default="")

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
        if self.side_effect_function:
            side_effect = import_string(self.side_effect_function)
            side_effect(review_obj=review_obj)


class ModelReview(BaseReview):
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
        app_label = "model_reviews"
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

    def send_review_complete_notification(self):
        """Send notification that review is complete."""
        if self.user and not self.needs_review():
            source = self.content_object
            if source.review_complete_notify_function:
                notify_func = import_string(source.review_complete_notify_function)
                notify_func(review_obj=self)


class Reviewer(BaseReview):
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

    class Meta:
        """Meta definition for Reviewer."""

        app_label = "model_reviews"
        verbose_name = _("Reviewer")
        verbose_name_plural = _("Reviewers")
        unique_together = [["user", "review"]]

    def __str__(self):
        """Unicode representation of Reviewer."""
        return f"{self.user} review for {self.review}"

    def send_request_for_review(self):
        """Send a notification for request to perform review."""
        if self.review.content_object:
            if self.review.content_object.request_for_review_function:
                notify_func = import_string(
                    self.review.content_object.request_for_review_function
                )
                notify_func(self)

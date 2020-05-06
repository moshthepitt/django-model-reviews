"""Models module for model reviews."""

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import gettext_lazy as _

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
    review_reason = models.TextField(_("Review Reason"), blank=True, default="")
    review_comments = models.TextField(_("Review Comments"), blank=True, default="")

    class Meta:
        """Meta definition for AbstractReview."""

        abstract = True


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
    sandbox = JSONField(
        _("Sandbox Data"), encoder=DjangoJSONEncoder, default=dict, blank=False
    )
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

"""Models module for approvals."""

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import gettext_lazy as _

USER = settings.AUTH_USER_MODEL


class AbstractApproval(models.Model):
    """Model definition for AbstractApproval."""

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
    review_date = models.DateTimeField(_("Review Date"))
    review_reason = models.TextField(_("Review Reason"), blank=True, default="")
    review_Comments = models.TextField(_("Review Comments"), blank=True, default="")

    class Meta:
        """Meta definition for AbstractApproval."""

        abstract = True


class Approval(AbstractApproval):
    """Model definition for Approval."""

    user = models.ForeignKey(
        USER,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        help_text=_("The user who submitted to request for approval"),
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
        verbose_name=_("Reviewer(s)"),
        through="Reviewer",
        through_fields=("user", "approval"),
    )

    class Meta:
        """Meta definition for Approval."""

        abstract = False
        verbose_name = _("Approval")
        verbose_name_plural = _("Approvals")
        indexes = [models.Index(fields=["content_type", "object_id"])]

    def __str__(self):
        """Unicode representation of Approval."""
        return "this"


class Reviewer(models.Model):
    """Model definition for Reviewer."""

    user = models.ForeignKey(USER, verbose_name=_("User"), on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)
    approval = models.ForeignKey(
        "Approval", verbose_name=_("Approval"), on_delete=models.CASCADE
    )
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
        return "this"

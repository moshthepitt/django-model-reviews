"""models module for test app."""

from django.contrib.auth.models import User
from django.db import models

from model_reviews.models import AbstractReview, Reviewer


class TestModel(AbstractReview):
    """Model definition for TestModel."""

    name = models.CharField(max_length=100)

    # model_review options
    side_effect_function = "tests.test_app.models.side_effects"

    class Meta:
        """Meta definition for TestModel."""

        abstract = False
        verbose_name = "TestModel"
        verbose_name_plural = "TestModels"

    def __str__(self):
        """Unicode representation of TestModel."""
        return self.name


class TestModel2(AbstractReview):
    """Model definition for TestModel."""

    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, default=None, blank=True
    )

    # model_review options
    set_reviewers_function = "tests.test_app.models.set_reviewers"


def side_effects(review_obj: models.Model):  # pylint: disable=unused-argument
    """
    Run side effects.

    This is a dummy side effects function, for testing.
    """
    return None


def set_reviewers(review_obj: models.Model):
    """Set reviewers."""
    try:
        user = User.objects.get(username="finalboss")
    except User.DoesNotExist:
        pass
    else:
        if not Reviewer.objects.filter(user=user, review=review_obj).exists():
            reviewer = Reviewer(user=user, review=review_obj)
            reviewer.save()

"""models module for test app."""

from django.db import models

from model_reviews.models import AbstractReview


class TestModel(AbstractReview):
    """Model definition for TestModel."""

    name = models.CharField(max_length=100)

    class Meta:
        """Meta definition for TestModel."""

        abstract = False
        verbose_name = "TestModel"
        verbose_name_plural = "TestModels"

    def __str__(self):
        """Unicode representation of TestModel."""
        return self.name

"""Test models."""
from django.test import TestCase

from model_mommy import mommy

from .test_app.models import TestModel


class TestCRUD(TestCase):
    """Test class for models."""

    def test_model_inheritance(self):
        """Test models inheritance of AbstractReview."""
        test_model = mommy.make("test_app.TestModel", name="Test 1")
        self.assertEqual(TestModel.PENDING, test_model.review_status)
        self.assertEqual(None, test_model.review_date)
        self.assertEqual("", test_model.review_reason)
        self.assertEqual("", test_model.review_comments)

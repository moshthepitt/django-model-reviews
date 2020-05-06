"""Test models."""
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from model_mommy import mommy

from model_reviews.models import ModelReview

from .test_app.models import TestModel


class TestCRUD(TestCase):
    """Test class for models."""

    def test_model_inheritance(self):
        """Test models inheritance of AbstractReview."""
        test_model = mommy.make("test_app.TestModel", name="Test 1")
        obj_type = ContentType.objects.get_for_model(test_model)

        self.assertEqual(TestModel.PENDING, test_model.review_status)
        self.assertEqual(None, test_model.review_date)
        self.assertEqual("", test_model.review_reason)
        self.assertEqual("", test_model.review_comments)

        review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)
        self.assertEqual(ModelReview.PENDING, test_model.review_status)
        self.assertEqual(None, review.review_date)
        self.assertEqual("", review.review_reason)
        self.assertEqual("", review.review_comments)

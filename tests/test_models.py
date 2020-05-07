"""Test models."""
from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

import pytz
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
        self.assertEqual(ModelReview.PENDING, review.review_status)
        self.assertEqual(None, review.review_date)
        self.assertEqual("", review.review_reason)
        self.assertEqual("", review.review_comments)

    def test_modelreview(self):
        """Test that you can do model reviews."""
        test_model = mommy.make("test_app.TestModel", name="Test 2")
        obj_type = ContentType.objects.get_for_model(test_model)
        review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)

        date = datetime(2017, 6, 5, 0, 0, 0, tzinfo=pytz.timezone(settings.TIME_ZONE))

        review.review_status = ModelReview.APPROVED
        review.review_date = date
        review.review_reason = "foo"
        review.review_comments = "bar"
        review.save()

        test_model.refresh_from_db()

        self.assertEqual(TestModel.APPROVED, test_model.review_status)
        self.assertEqual(date, review.review_date)
        self.assertEqual("foo", review.review_reason)
        self.assertEqual("bar", review.review_comments)

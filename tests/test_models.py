"""Test models."""
from datetime import datetime
from unittest.mock import patch

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

import pytz
from model_mommy import mommy

from model_reviews.constants import SANDBOX_FIELD
from model_reviews.models import ModelReview, Reviewer

from .test_app.models import TestModel


class TestModels(TestCase):
    """Test class for models."""

    @patch("tests.test_app.models.set_reviewers")
    @patch("model_reviews.side_effects.set_review_user")
    def test_model_inheritance(self, set_reviewers_mock, set_review_user_mock):
        """Test models inheritance of AbstractReview."""
        test_model = mommy.make("test_app.TestModel", name="Test 1")
        obj_type = ContentType.objects.get_for_model(test_model)

        self.assertEqual(TestModel.PENDING, test_model.review_status)
        self.assertEqual(None, test_model.review_date)

        review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)
        self.assertEqual(ModelReview.PENDING, review.review_status)
        self.assertEqual(None, review.review_date)
        self.assertEqual(None, review.user)

        # test with a model that has a user
        user = mommy.make("auth.User", username="Test1")
        test_model2 = mommy.make("test_app.TestModel2", user=user)
        review2 = ModelReview.objects.get(
            content_type=ContentType.objects.get_for_model(test_model2),
            object_id=test_model2.id,
        )
        # assert that mocks are called with the expected params
        review2.refresh_from_db()
        set_review_user_mock.assert_called_with(review_obj=review2)
        set_reviewers_mock.assert_called_with(review_obj=review2)

    def test_set_user_function(self):
        """Test that the set_user_function mechanism works."""
        user = mommy.make("auth.User", username="Test1")
        test_model2 = mommy.make("test_app.TestModel2", user=user)
        review2 = ModelReview.objects.get(
            content_type=ContentType.objects.get_for_model(test_model2),
            object_id=test_model2.id,
        )
        self.assertEqual(user, review2.user)

    def test_set_reviewers_function(self):
        """Test that the set_reviewers_function mechanism works."""
        user = mommy.make("auth.User", username="Test1")
        finalboss = mommy.make("auth.User", username="finalboss")

        test_model2 = mommy.make("test_app.TestModel2", user=user)
        review2 = ModelReview.objects.get(
            content_type=ContentType.objects.get_for_model(test_model2),
            object_id=test_model2.id,
        )
        self.assertTrue(
            Reviewer.objects.filter(user=finalboss, review=review2).exists()
        )

    @patch("tests.test_app.models.side_effects")
    def test_modelreview_approval(self, mock):
        """Test that you can do model review approvals."""
        test_model = mommy.make("test_app.TestModel", name="Test 2")
        obj_type = ContentType.objects.get_for_model(test_model)
        review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)

        date = datetime(2017, 6, 5, 0, 0, 0, tzinfo=pytz.timezone(settings.TIME_ZONE))

        review.review_status = ModelReview.APPROVED
        review.review_date = date
        review.save()

        test_model.refresh_from_db()

        self.assertEqual(TestModel.APPROVED, test_model.review_status)
        self.assertEqual(date, test_model.review_date)

        # assert that mock is called with the expected params
        review.refresh_from_db()
        mock.assert_called_once_with(review_obj=review)

    @patch("tests.test_app.models.side_effects")
    def test_modelreview_rejection(self, mock):
        """Test that you can do model review rejections."""
        test_model = mommy.make("test_app.TestModel", name="Test 2")
        obj_type = ContentType.objects.get_for_model(test_model)
        review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)

        date = datetime(2017, 6, 5, 0, 0, 0, tzinfo=pytz.timezone(settings.TIME_ZONE))

        review.review_status = ModelReview.REJECTED
        review.review_date = date
        review.save()

        test_model.refresh_from_db()

        self.assertEqual(TestModel.REJECTED, test_model.review_status)
        self.assertEqual(date, test_model.review_date)

        # assert that mock is called with the expected params
        review.refresh_from_db()
        mock.assert_called_once_with(review_obj=review)

    def test_reviewed_obj_update(self):  # pylint: disable=too-many-statements
        """Test what happens when reviewed object is updated."""
        test_model = mommy.make("test_app.TestModel", name="Test 3")
        obj_type = ContentType.objects.get_for_model(test_model)
        review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)

        # when other fields are updated
        test_model.name = "Used to be Test 3"
        test_model.save()

        review.refresh_from_db()
        self.assertEqual(ModelReview.PENDING, review.review_status)
        self.assertEqual(None, review.review_date)

        # when reviewed object is directly approved
        approve_date = datetime(
            2017, 6, 5, 0, 0, 0, tzinfo=pytz.timezone(settings.TIME_ZONE)
        )
        test_model.review_status = TestModel.APPROVED
        test_model.review_date = approve_date
        test_model.save()

        review.refresh_from_db()  # nothing changed on the review but sandbox updated
        self.assertEqual(ModelReview.PENDING, review.review_status)
        self.assertEqual(None, review.review_date)
        self.assertEqual(
            ModelReview.APPROVED, review.data[SANDBOX_FIELD]["review_status"]
        )
        self.assertEqual(
            "2017-06-05T00:00:00+02:27", review.data[SANDBOX_FIELD]["review_date"]
        )

        test_model.refresh_from_db()  # nothing changed on the reviewed model
        self.assertEqual(ModelReview.PENDING, test_model.review_status)
        self.assertEqual(None, test_model.review_date)
        self.assertEqual("Used to be Test 3", test_model.name)

        # when reviewed object is directly rejected
        reject_date = datetime(
            2017, 6, 6, 0, 0, 0, tzinfo=pytz.timezone(settings.TIME_ZONE)
        )
        test_model.review_status = TestModel.REJECTED
        test_model.review_date = reject_date
        test_model.save()

        review.refresh_from_db()  # nothing changed on the review but sandbox updated
        self.assertEqual(ModelReview.PENDING, review.review_status)
        self.assertEqual(None, review.review_date)
        self.assertEqual(
            ModelReview.REJECTED, review.data[SANDBOX_FIELD]["review_status"]
        )
        self.assertEqual(
            "2017-06-06T00:00:00+02:27", review.data[SANDBOX_FIELD]["review_date"]
        )

        test_model.refresh_from_db()  # nothing changed on the reviewed model
        self.assertEqual(ModelReview.PENDING, test_model.review_status)
        self.assertEqual(None, test_model.review_date)
        self.assertEqual("Used to be Test 3", test_model.name)

        # and no other review objects were created
        self.assertEqual(
            1,
            ModelReview.objects.filter(
                content_type=obj_type, object_id=test_model.id
            ).count(),
        )

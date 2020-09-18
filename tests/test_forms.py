"""Test forms."""
from datetime import datetime
from unittest.mock import patch

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, TestCase

import pytz
from model_mommy import mommy

from model_reviews.forms import PerformReview
from model_reviews.models import ModelReview


class TestForms(TestCase):
    """Test class for forms."""

    def setUp(self):
        """Set up test class."""
        self.factory = RequestFactory()

    @patch("django.utils.timezone.now")
    def test_successful_performreview(self, mock):
        """Test successful PerformReview submission."""
        mocked_now = datetime(2010, 1, 1, tzinfo=pytz.timezone(settings.TIME_ZONE))
        mock.return_value = mocked_now

        user1 = mommy.make("auth.User", username="joe")
        user2 = mommy.make("auth.User", username="jane")

        test_model = mommy.make("test_app.TestModel", name="Test")
        obj_type = ContentType.objects.get_for_model(test_model)

        review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)
        review.user = user1
        review.save()

        reviewer = mommy.make("model_reviews.Reviewer", user=user2, review=review)

        request = self.factory.get("/")
        request.session = {}
        request.user = user2

        data = {
            "review": review.pk,
            "reviewer": reviewer.pk,
            "review_status": ModelReview.APPROVED,
        }

        form = PerformReview(data=data)
        self.assertTrue(form.is_valid())
        form.save()

        review.refresh_from_db()
        reviewer.refresh_from_db()
        test_model.refresh_from_db()

        self.assertEqual(ModelReview.APPROVED, review.review_status)
        self.assertEqual(ModelReview.APPROVED, test_model.review_status)
        self.assertEqual(mocked_now, review.review_date)
        self.assertEqual(mocked_now, test_model.review_date)

        self.assertEqual(True, reviewer.reviewed)
        self.assertEqual(mocked_now, reviewer.review_date)
        self.assertEqual(ModelReview.APPROVED, reviewer.review_status)

    @patch("django.utils.timezone.now")
    def test_successful_performreview_multiple_reviewers(self, mock):
        """Test successful PerformReview submission with multiple reviewers."""
        mocked_now = datetime(2010, 1, 1, tzinfo=pytz.timezone(settings.TIME_ZONE))
        mock.return_value = mocked_now

        user1 = mommy.make("auth.User", username="joe")
        user2 = mommy.make("auth.User", username="jane")
        user3 = mommy.make("auth.User", username="jenny")

        test_model = mommy.make("test_app.TestModel", name="Test")
        obj_type = ContentType.objects.get_for_model(test_model)

        review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)
        review.user = user1
        review.save()

        mommy.make("model_reviews.Reviewer", user=user2, review=review)
        reviewer = mommy.make("model_reviews.Reviewer", user=user3, review=review)

        request = self.factory.get("/")
        request.session = {}
        request.user = user3

        data = {
            "review": review.pk,
            "reviewer": reviewer.pk,
            "review_status": ModelReview.APPROVED,
        }

        form = PerformReview(data=data)
        self.assertTrue(form.is_valid())
        form.save()

        review.refresh_from_db()
        reviewer.refresh_from_db()
        test_model.refresh_from_db()

        self.assertEqual(ModelReview.APPROVED, review.review_status)
        self.assertEqual(ModelReview.APPROVED, test_model.review_status)
        self.assertEqual(mocked_now, review.review_date)
        self.assertEqual(mocked_now, test_model.review_date)

        self.assertEqual(True, reviewer.reviewed)
        self.assertEqual(mocked_now, reviewer.review_date)
        self.assertEqual(ModelReview.APPROVED, reviewer.review_status)

    # pylint: disable=too-many-locals
    @patch("tests.test_app.models.get_next_reviewers")
    @patch("django.utils.timezone.now")
    def test_successful_performreview_multiple_reviewers_levels(self, mock, next_mock):
        """Test successful PerformReview with multiple reviewers of different levels."""
        mocked_now = datetime(2010, 1, 1, tzinfo=pytz.timezone(settings.TIME_ZONE))
        mock.return_value = mocked_now

        user1 = mommy.make("auth.User", username="joe")
        user2 = mommy.make("auth.User", username="jane")
        user3 = mommy.make("auth.User", username="jenny")

        test_model = mommy.make("test_app.TestModel", name="Test")
        obj_type = ContentType.objects.get_for_model(test_model)

        review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)
        review.user = user1
        review.save()

        reviewer = mommy.make(
            "model_reviews.Reviewer", user=user2, review=review, level=1
        )
        reviewer2 = mommy.make(
            "model_reviews.Reviewer", user=user3, review=review, level=2
        )

        request = self.factory.get("/")
        request.session = {}
        request.user = user2

        data = {
            "review": review.pk,
            "reviewer": reviewer.pk,
            "review_status": ModelReview.APPROVED,
        }

        form = PerformReview(data=data)
        self.assertTrue(form.is_valid())
        form.save()

        review.refresh_from_db()
        reviewer.refresh_from_db()
        test_model.refresh_from_db()

        next_mock.assert_called_once_with(review_obj=review)

        self.assertEqual(ModelReview.PENDING, review.review_status)
        self.assertEqual(ModelReview.PENDING, test_model.review_status)
        self.assertEqual(None, review.review_date)
        self.assertEqual(None, test_model.review_date)

        self.assertEqual(True, reviewer.reviewed)
        self.assertEqual(mocked_now, reviewer.review_date)
        self.assertEqual(ModelReview.APPROVED, reviewer.review_status)

        request = self.factory.get("/")
        request.session = {}
        request.user = user3

        data2 = {
            "review": review.pk,
            "reviewer": reviewer2.pk,
            "review_status": ModelReview.APPROVED,
        }

        form = PerformReview(data=data2)
        self.assertTrue(form.is_valid())
        form.save()

        review.refresh_from_db()
        reviewer2.refresh_from_db()
        test_model.refresh_from_db()

        self.assertEqual(ModelReview.APPROVED, review.review_status)
        self.assertEqual(ModelReview.APPROVED, test_model.review_status)
        self.assertEqual(mocked_now, review.review_date)
        self.assertEqual(mocked_now, test_model.review_date)

        self.assertEqual(True, reviewer2.reviewed)
        self.assertEqual(mocked_now, reviewer2.review_date)
        self.assertEqual(ModelReview.APPROVED, reviewer2.review_status)

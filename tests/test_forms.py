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
        request.user = user1

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

        self.assertEqual(True, reviewer.reviewed)
        self.assertEqual(mocked_now, reviewer.review_date)

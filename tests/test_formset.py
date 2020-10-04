"""Test forms."""
from datetime import datetime
from unittest.mock import patch

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory

import pytz
from model_mommy import mommy
from snapshottest.django import TestCase

from model_reviews.formset import get_review_formset
from model_reviews.models import ModelReview, Reviewer


class TestForms(TestCase):
    """Test class for forms."""

    maxDiff = None

    def setUp(self):
        """Set up test class."""
        self.factory = RequestFactory()

    @patch("django.utils.timezone.now")
    def test_model_review_formset(self, mock):
        """Test model review formset."""
        mocked_now = datetime(2010, 1, 1, tzinfo=pytz.timezone(settings.TIME_ZONE))
        mock.return_value = mocked_now

        user1 = mommy.make("auth.User", username="joe")
        user2 = mommy.make("auth.User", username="jane")

        for i in range(1, 4):
            test_model = mommy.make("test_app.TestModel", name="Test")
            obj_type = ContentType.objects.get_for_model(test_model)
            review = ModelReview.objects.get(
                content_type=obj_type, object_id=test_model.id
            )
            # we want to control the pk so we force create a new review
            ModelReview.objects.get(
                content_type=obj_type, object_id=test_model.id
            ).delete()
            review = mommy.make(
                "model_reviews.ModelReview",
                content_type=obj_type,
                object_id=test_model.id,
                id=1337 + i,
            )

            review.user = user1
            review.save()

            mommy.make("model_reviews.Reviewer", user=user2, review=review, id=1337 + i)

        formset_class = get_review_formset(user=user2)

        self.assertMatchSnapshot(formset_class().as_table())

        data = {
            "form-TOTAL_FORMS": 3,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 0,
            "form-MAX_NUM_FORMS": 3,
        }

        for idx, review in enumerate(ModelReview.objects.filter(user=user1)):
            data[f"form-{idx}-review_status"] = ModelReview.APPROVED
            data[f"form-{idx}-reviewer"] = Reviewer.objects.get(review=review).pk
            data[f"form-{idx}-review"] = review.pk

        formset = formset_class(data=data)

        self.assertTrue(formset.is_valid())

        for form in formset:
            form.save()

        for review in ModelReview.objects.filter(user=user1):
            reviewer = Reviewer.objects.get(review=review)

            self.assertEqual(ModelReview.APPROVED, review.review_status)
            self.assertEqual(ModelReview.APPROVED, review.content_object.review_status)
            self.assertEqual(mocked_now, review.review_date)
            self.assertEqual(mocked_now, review.content_object.review_date)

            self.assertEqual(True, reviewer.reviewed)
            self.assertEqual(mocked_now, reviewer.review_date)
            self.assertEqual(ModelReview.APPROVED, reviewer.review_status)

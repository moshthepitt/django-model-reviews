"""Test the views."""
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings

from model_mommy import mommy

from model_reviews import constants
from model_reviews.forms import PerformReview
from model_reviews.models import ModelReview
from model_reviews.views import ReviewDisplay


@override_settings(ROOT_URLCONF="tests.test_app.urls")
class TestViews(TestCase):
    """Test class for views."""

    maxDiff = None

    def setUp(self):
        """Set up."""
        super().setUp()
        self.user = mommy.make("auth.User", username="mosh")
        self.reviewer = mommy.make("auth.User", username="neemo")

    def test_review_display(self):
        """Test that a review's details are displayed ok."""
        test_model = mommy.make("test_app.TestModel", name="Test 1")
        obj_type = ContentType.objects.get_for_model(test_model)
        review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)
        mommy.make("model_reviews.Reviewer", user=self.reviewer, review=review)

        res = self.client.get(f"/review/{review.pk}")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["view"], ReviewDisplay)
        self.assertIsInstance(res.context["form"], PerformReview)
        self.assertTemplateUsed(res, "model_reviews/modelreview_detail.html")

    def test_review_form(self):
        """Test that a review's form works ok."""
        test_model = mommy.make("test_app.TestModel", name="Test 1")
        obj_type = ContentType.objects.get_for_model(test_model)
        review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)
        reviewer = mommy.make(
            "model_reviews.Reviewer", user=self.reviewer, review=review
        )

        data = {
            "review": review.pk,
            "reviewer": reviewer.pk,
            "review_status": ModelReview.APPROVED,
        }

        res = self.client.post(f"/review/{review.pk}", data)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/")

        test_model.refresh_from_db()
        self.assertEqual(ModelReview.APPROVED, test_model.review_status)
        self.assertFalse(test_model.review_date is None)
        self.assertTrue(
            constants.REVIEW_FORM_SUCCESS_MSG in res.cookies["messages"].value
        )

"""Test HTML output."""
from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.test import override_settings

from model_mommy import mommy
from snapshottest.django import TestCase

from model_reviews.models import ModelReview


@override_settings(ROOT_URLCONF="tests.test_app.urls")
class TestHTML(TestCase):
    """Test class for HTML tests."""

    maxDiff = None

    @patch("django.middleware.csrf.get_token")
    def test_initial_form(self, csrf_mock):
        """Test the initial form before anything is done."""
        csrf_mock.return_value = "CSRF-I_LOVE-OOV"

        test_model = mommy.make(
            "test_app.TestModel",
            name="Test 1",
            review_reason="Taking some time off after the current Reveal contract(s) come to an end.",  # noqa  # pylint:disable=line-too-long
        )
        obj_type = ContentType.objects.get_for_model(test_model)
        review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)

        res = self.client.get(f"/review/{review.pk}")
        self.assertMatchSnapshot(res.content.decode("utf-8"))

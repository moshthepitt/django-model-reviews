"""Test emails."""
from unittest.mock import call, patch

from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.test import TestCase

from model_mommy import mommy

from model_reviews.emails import get_display_name, send_email
from model_reviews.models import ModelReview


class TestEmails(TestCase):
    """Test class for emails."""

    def test_get_display_name(self):
        """Test get_display_name."""
        self.assertEqual(
            "Mosh Pitt",
            get_display_name(
                mommy.make("auth.User", first_name="Mosh", last_name="Pitt")
            ),
        )
        self.assertEqual(
            "mosh", get_display_name(mommy.make("auth.User", first_name="mosh"))
        )
        self.assertEqual(
            "Pitt", get_display_name(mommy.make("auth.User", last_name="Pitt"))
        )
        self.assertEqual(
            "xiaou", get_display_name(mommy.make("auth.User", username="xiaou"))
        )

    @patch("model_reviews.emails.send_email")
    def test_emails_asking_for_review(self, mock):
        """Test that emails are sent asking for review."""
        test_model = mommy.make("test_app.TestModel")
        obj_type = ContentType.objects.get_for_model(test_model)
        review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)

        mommy.make(
            "model_review.Reviewer",
            user=mommy.make("auth.User", username="r1", email="r1@example.com"),
            review=review,
        )

        mommy.make(
            "model_review.Reviewer",
            user=mommy.make(
                "auth.User",
                username="r2",
                email="r2@example.com",
                first_name="Jane",
                last_name="Doe",
            ),
            review=review,
        )

        self.assertEqual(2, mock.call_count)

        expected_calls = [
            call(
                "name",
                "email",
                "subject",
                "message",
                "obj",
                "cc",
                "template",
                "template_path",
            ),
            call(
                "name",
                "email",
                "subject",
                "message",
                "obj",
                "cc",
                "template",
                "template_path",
            ),
        ]

        mock.assert_has_calls(expected_calls)

    @patch("model_reviews.emails.send_email")
    def test_emails_after_review(self, mock):
        """Test that emails are after review is complete."""
        # test_model = mommy.make(
        #     "test_app.TestModel",
        #     user=mommy.make("auth.User", username="guy1", email="g1@example.com")
        # )
        # obj_type = ContentType.objects.get_for_model(test_model)
        # review = ModelReview.objects.get(content_type=obj_type, object_id=test_model.id)

        self.assertEqual(1, mock.call_count)
        expected_calls = [
            call(
                "name",
                "email",
                "subject",
                "message",
                "obj",
                "cc",
                "template",
                "template_path",
            )
        ]

        mock.assert_has_calls(expected_calls)

    def test_send_email(self):
        """
        Test send_email
        """

        message = "The quick brown fox."

        data = {
            "name": "Bob Munro",
            "email": "bob@example.com",
            "subject": "I love oov",
            "message": message,
            "cc_list": ["admin@example.com"],
        }

        send_email(**data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "I love oov")
        self.assertEqual(mail.outbox[0].to, ["Bob Munro <bob@example.com>"])
        self.assertEqual(mail.outbox[0].cc, ["admin@example.com"])
        self.assertEqual(
            mail.outbox[0].body,
            "Hello Bob Munro,\n\nThe quick brown fox.\n\nThank you,\n\n"
            "example.com\n------\nhttp://example.com\n",
        )
        self.assertEqual(
            mail.outbox[0].alternatives[0][0],
            "Hello Bob Munro,<br/><br/><p>The quick brown fox.</p><br/><br/>"
            "Thank you,<br/>example.com<br/>------<br/>http://example.com",
        )

    @patch("model_reviews.emails.Site.objects.get_current")
    @patch("model_reviews.emails.render_to_string")
    def test_send_email_templates(self, mock, site_mock):  # pylint: disable=no-self-use
        """Test the templates used with send_email."""
        mock.return_value = "Some random text"
        site_mock.return_value = 42  # ensure that this is predictable

        # test generic
        data = {
            "name": "Bob Munro",
            "email": "bob@example.com",
            "subject": "I love oov",
            "message": "Its dangerous",
        }

        send_email(**data)

        context = data.copy()
        context.pop("email")
        context["object"] = None
        context["SITE"] = 42

        expected_calls = [
            call("model_reviews/email/generic_email_subject.txt", context),
            call("model_reviews/email/generic_email_body.txt", context),
            call("model_reviews/email/generic_email_body.html", context),
        ]

        mock.assert_has_calls(expected_calls)
        mock.reset_mock()

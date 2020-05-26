"""Test emails."""
from unittest.mock import call, patch

from django.core import mail
from django.test import TestCase

from model_reviews.emails import send_email


class TestEmails(TestCase):
    """Test class for emails."""

    # def test_emails_asking_for_review(self):
    #     """Test that emails are sent asking for review."""
    #     self.fail()

    # def test_emails_after_review(self):
    #     """Test that emails are after review is complete."""
    #     self.fail()

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

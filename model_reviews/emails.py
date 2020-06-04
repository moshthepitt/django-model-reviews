"""Emails module for model_review."""
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from model_reviews.constants import EMAIL_TEMPLATE, EMAIL_TEMPLATE_PATH
from model_reviews.models import ModelReview, Reviewer


def get_display_name(user: User):
    """Get display name from user object."""
    if any((user.first_name, user.last_name)):
        return user.get_full_name()

    return user.username


def send_email(  # pylint: disable=too-many-arguments,too-many-locals,bad-continuation
    name: str,
    email: str,
    subject: str,
    message: str,
    obj: object = None,
    cc_list: list = None,
    template: str = EMAIL_TEMPLATE,
    template_path: str = EMAIL_TEMPLATE_PATH,
):
    """
    Send a generic email.

    :param name: name of person
    :param email: email address to send to
    :param subject: the email's subject
    :param message: the email's body text
    :param obj: the object in question
    :param cc_list: the list of email address to "CC"
    :param template: the template to use
    """
    context = {
        "name": name,
        "subject": subject,
        "message": message,
        "object": obj,
        "SITE": Site.objects.get_current(),
    }
    email_subject = render_to_string(
        f"{template_path}/{template}_email_subject.txt", context
    ).replace("\n", "")
    email_txt_body = render_to_string(
        f"{template_path}/{template}_email_body.txt", context
    )
    email_html_body = render_to_string(
        f"{template_path}/{template}_email_body.html", context
    ).replace("\n", "")

    subject = email_subject
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = f"{name} <{email}>"
    text_content = email_txt_body
    html_content = email_html_body
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    if cc_list:
        msg.cc = cc_list
    msg.attach_alternative(html_content, "text/html")

    return msg.send(fail_silently=True)


def send_request_for_review(review_obj: ModelReview):
    """Send email requesting a review."""
    reviewers = Reviewer.objects.filter(review=review_obj, reviewed=False)
    for reviewer in reviewers:
        send_single_request_for_review(reviewer)


def send_single_request_for_review(reviewer: Reviewer):
    """Send email requesting a review to one reviewer."""
    if reviewer.user.email:
        source = reviewer.review.content_object
        send_email(
            name=get_display_name(reviewer.user),
            email=reviewer.user.email,
            subject=source.review_request_email_subject,
            message=source.review_request_email_body,
            obj=reviewer.review,
            cc_list=None,
            template=source.email_template,
            template_path=source.email_template_path,
        )


def send_review_complete_notice(review_obj: ModelReview):
    """Send notice that review is complete."""
    if not review_obj.needs_review() and review_obj.user:
        if review_obj.user.email:
            source = review_obj.content_object
            send_email(
                name=get_display_name(review_obj.user),
                email=review_obj.user.email,
                subject=source.review_complete_email_subject,
                message=source.review_complete_email_body,
                obj=review_obj,
                cc_list=None,
                template=source.email_template,
                template_path=source.email_template_path,
            )

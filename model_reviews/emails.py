"""Emails module for model_review."""
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email(  # pylint: disable=too-many-arguments,too-many-locals,bad-continuation
    name: str,
    email: str,
    subject: str,
    message: str,
    obj: object = None,
    cc_list: list = None,
    template: str = "generic",
    template_path: str = "model_reviews/email",
):
    """
    Sends a generic email

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

"""forms module for model_reviews."""
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from model_reviews.constants import (
    REVIEW_FORM_WRONG_REVIEW_MSG,
    REVIEW_FORM_WRONG_REVIEWER_MSG,
    REVIEW_FORM_WRONG_STATUS_MSG,
)
from model_reviews.models import ModelReview, Reviewer
from model_reviews.utils import perform_review


class PerformReview(forms.Form):
    """PerformReview Form definition."""

    review = forms.ModelChoiceField(queryset=ModelReview.objects.all())
    reviewer = forms.ModelChoiceField(queryset=Reviewer.objects.all())
    review_status = forms.ChoiceField(
        label=_(settings.MODELREVIEW_FORM_STATUS_FIELD_LABEL),
        choices=ModelReview.STATUS_CHOICES,
        required=True,
        error_messages={
            "invalid_choice": REVIEW_FORM_WRONG_STATUS_MSG,
            "required": REVIEW_FORM_WRONG_STATUS_MSG,
        },
    )

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop("request", None)
        self.vega_extra_kwargs = kwargs.pop(
            getattr(settings, "VEGA_MODELFORM_KWARG", "vega_extra_kwargs"), dict()
        )

    def clean_review_status(self):
        """Clean review_status."""
        data = self.cleaned_data["review_status"]
        if data == ModelReview.PENDING:
            raise forms.ValidationError(REVIEW_FORM_WRONG_STATUS_MSG)
        return data

    def save(self):
        """Save the form."""
        data = self.cleaned_data
        review = data["review"]
        reviewer = data["reviewer"]
        now = timezone.now()
        with transaction.atomic():
            # save reviewer stuff
            reviewer.reviewed = True
            reviewer.review_date = now
            reviewer.review_status = data["review_status"]
            reviewer.save()
            # perform the review
            perform_review(review=review)


def get_review_form(review: ModelReview, user: User):
    """Get review form for a particular review object."""
    review_qs = ModelReview.objects.filter(id=review.id)
    reviewer_qs = Reviewer.objects.filter(review=review)
    initial_reviewer = None
    if not user.is_anonymous:
        reviewer_qs = reviewer_qs.filter(user=user)
        first_reviewer = reviewer_qs.first()
        if first_reviewer:
            initial_reviewer = first_reviewer.pk

    return type(
        "PerformReviewForm",
        (PerformReview,),
        {
            "review": forms.ModelChoiceField(
                initial=review_qs.first().pk,
                queryset=review_qs,
                widget=forms.HiddenInput,
                required=True,
                error_messages={
                    "invalid_choice": REVIEW_FORM_WRONG_REVIEW_MSG,
                    "required": REVIEW_FORM_WRONG_REVIEW_MSG,
                },
            ),
            "reviewer": forms.ModelChoiceField(
                queryset=reviewer_qs,
                initial=initial_reviewer,
                widget=forms.HiddenInput,
                required=True,
                error_messages={
                    "invalid_choice": REVIEW_FORM_WRONG_REVIEWER_MSG,
                    "required": REVIEW_FORM_WRONG_REVIEWER_MSG,
                },
            ),
        },
    )

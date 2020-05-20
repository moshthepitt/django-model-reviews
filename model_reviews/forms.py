"""forms module for model_reviews."""
from django import forms
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from model_reviews.models import ModelReview, Reviewer


class PerformReview(forms.Form):
    """PerformReview Form definition."""

    review = forms.ModelChoiceField(
        queryset=ModelReview.objects.all(), widget=forms.HiddenInput, required=True
    )
    reviewer = forms.ModelChoiceField(
        queryset=Reviewer.objects.all(), widget=forms.HiddenInput, required=True
    )
    review_status = forms.ChoiceField(
        label=_(settings.MODELREVIEW_FORM_STATUS_FIELD_LABEL),
        choices=ModelReview.STATUS_CHOICES,
        required=True,
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
            raise forms.ValidationError(
                settings.MODELREVIEW_FORM_REVIEW_STATUS_VALIDATION_MSG
            )
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
            reviewer.save()
            # save review
            review.review_status = data["review_status"]
            review.save()

"""forms module for model_reviews"""
from django import forms
from django.conf import settings
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
    review_reason = forms.CharField(
        label=_(settings.MODELREVIEW_FORM_REASON_FIELD_LABEL),
        widget=forms.Textarea,
        required=False,
    )
    review_comments = forms.CharField(
        label=_(settings.MODELREVIEW_FORM_COMMENTS_FIELD_LABEL),
        widget=forms.Textarea,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super().__init__(*args, **kwargs)
        self.request = kwargs.pop("request", None)
        self.vega_extra_kwargs = kwargs.pop(settings.VEGA_MODELFORM_KWARG, dict())

    def clean_review_status(self):
        """Clean review_status."""
        data = self.cleaned_data["review_status"]
        if data == ModelReview.PENDING:
            raise forms.ValidationError(
                settings.MODELREVIEW_FORM_REVIEW_STATUS_VALIDATION_MSG
            )
        return data

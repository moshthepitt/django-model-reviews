"""forms module for model_reviews."""
from typing import List, Optional, Union

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import QuerySet
from django.forms import BaseFormSet, formset_factory
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


class ModelReviewFormSet(BaseFormSet):
    """
    Custom BaseFormSet for model reviews.

    We basically want to make it possibly to pass in a list of form classes
    that will be used to generate the formset.
    """

    def __init__(self, form_list: List[PerformReview], *args, **kwargs):
        """
        Initialize.

        The only thing that we want to do here is add "form_list" as a kwarg
        """
        self.form_list = form_list or []
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        """
        Instantiate and return the i-th form instance in a formset.

        We are modifying this function by adding the ability of getting the form
        from self.form_list.
        """
        defaults = {
            "auto_id": self.auto_id,
            "prefix": self.add_prefix(i),
            "error_class": self.error_class,
            # Don't render the HTML 'required' attribute as it may cause
            # incorrect validation for extra, optional, and deleted
            # forms in the formset.
            "use_required_attribute": False,
        }
        if self.is_bound:
            defaults["data"] = self.data
            defaults["files"] = self.files
        if self.initial and "initial" not in kwargs:
            try:
                defaults["initial"] = self.initial[i]
            except IndexError:
                pass
        # Allow extra forms to be empty, unless they're part of the minimum forms.
        # pylint: disable=no-member
        if i >= self.initial_form_count() and i >= self.min_num:
            defaults["empty_permitted"] = True
        defaults.update(kwargs)

        # this is the custom part of this sub-classed method
        try:
            form_class = self.form_list[i]
        except IndexError:
            form = self.form(**defaults)  # pylint: disable=no-member
        else:
            form = form_class(**defaults)
        # the custom part ends here

        self.add_fields(form, i)
        return form


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


def get_review_formset(  # pylint: disable=bad-continuation
    user: User, queryset: Optional[Union[QuerySet, List[ModelReview]]] = None
):
    """
    Get a formset of review forms.

    This is useful for doing bulk reviews.
    """
    if queryset is None:
        try:
            queryset = ModelReview.objects.filter(
                reviewer__user=user, review_status=ModelReview.PENDING
            )
        except TypeError:
            # this most likely means that the user is AnonymousUser
            queryset = ModelReview.objects.none()

    ReviewFormSet = formset_factory(
        form=PerformReview,
        formset=ModelReviewFormSet,
        extra=queryset.count(),
        max_num=queryset.count(),
    )
    review_forms: List[PerformReview] = []
    for item in queryset:
        review_form = get_review_form(review=item, user=user)
        review_forms.append(review_form)

    return ReviewFormSet(form_list=review_forms)

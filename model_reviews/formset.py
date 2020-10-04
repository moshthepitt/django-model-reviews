"""formset module for model_reviews."""
from typing import List, Optional, Union

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.forms import BaseFormSet

from model_reviews.forms import PerformReview, get_review_form
from model_reviews.models import ModelReview


class ModelReviewFormSet(BaseFormSet):
    """
    Custom BaseFormSet for model reviews.

    We basically want to make it possibly to pass in a list of form classes
    that will be used to generate the formset.
    """

    def __init__(  # pylint: disable=keyword-arg-before-vararg,bad-continuation
        self, form_list: Optional[List[PerformReview]] = None, *args, **kwargs
    ):
        """
        Initialize.

        The only thing that we want to do here is add "form_list" as a kwarg
        """
        # self.form_list is from model_review_formset_factory
        self.form_list: List[PerformReview] = form_list or self.form_list or []
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


def model_review_formset_factory(  # pylint: disable=bad-continuation,too-many-arguments
    form,
    form_list: List[PerformReview],
    formset=ModelReviewFormSet,
    extra=1,
    can_order=False,
    can_delete=False,
    max_num=0,
    validate_max=True,
    min_num=0,
    validate_min=False,
):
    """
    Return a FormSet for the given form class.

    This is based on django.forms.formset_factory and basically just adds form_list
    to the FormSet class.
    """
    attrs = {
        "form": form,
        "form_list": form_list,
        "extra": extra,
        "can_order": can_order,
        "can_delete": can_delete,
        "min_num": min_num,
        "max_num": max_num,
        "absolute_max": max_num,
        "validate_min": validate_min,
        "validate_max": validate_max,
    }
    return type(form.__name__ + "FormSet", (formset,), attrs)


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

    review_forms: List[PerformReview] = []
    for item in queryset:
        review_form = get_review_form(review=item, user=user)
        review_forms.append(review_form)

    ReviewFormSet = model_review_formset_factory(
        form=PerformReview,
        form_list=review_forms,
        formset=ModelReviewFormSet,
        extra=queryset.count(),
        max_num=queryset.count(),
    )

    return ReviewFormSet

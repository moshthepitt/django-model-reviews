"""Views module for model reviews."""
from typing import List, Optional

from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView, FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin

from braces.views import FormInvalidMessageMixin, FormValidMessageMixin, MessageMixin

from model_reviews.constants import (
    REVIEW_FORM_FAIL_MSG,
    REVIEW_FORM_SUCCESS_MSG,
    REVIEW_FORMSET_FAIL_MSG,
    REVIEW_FORMSET_SUCCESS_MSG,
)
from model_reviews.forms import get_review_form
from model_reviews.formset import get_review_formset
from model_reviews.models import ModelReview


class ReviewFormMixin:  # pylint: disable=too-few-public-methods
    """Mixin that implements a method to get review form."""

    model = ModelReview
    template_name = "model_reviews/modelreview_detail.html"

    def get_form_class(self):
        """Return the form class to use."""
        return get_review_form(review=self.get_object(), user=self.request.user)


class ReviewDisplay(ReviewFormMixin, DetailView):
    """Detailview for a model review object."""

    def get_context_data(self, **kwargs):
        """Get context data."""
        context = super().get_context_data(**kwargs)
        form_class = self.get_form_class()
        context["form"] = form_class()
        return context


class ReviewForm(  # pylint: disable=bad-continuation
    FormInvalidMessageMixin,
    FormValidMessageMixin,
    ReviewFormMixin,
    SingleObjectMixin,
    FormView,
):
    """FormView for a review."""

    form_invalid_message = _(REVIEW_FORM_FAIL_MSG)
    form_valid_message = _(REVIEW_FORM_SUCCESS_MSG)

    def post(self, request, *args, **kwargs):
        """Set self.object."""
        self.object = (  # pylint: disable=attribute-defined-outside-init
            self.get_object()
        )
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        """Get the success url."""
        return "/"

    def form_valid(self, form):
        """If the form is valid, save the review."""
        form.save()
        return super().form_valid(form)


class ReviewView(View):
    """
    View used to display details of a ModelReview object.

    This view shows both the model review object details as well as handles the
    form to perform a review.

    The structure is inspired by:
        https://docs.djangoproject.com/en/3.0/topics/class-based-views/mixins/#an-alternative-better-solution
    """

    def get(self, request, *args, **kwargs):
        """Get the ReviewDisplay view."""
        view = ReviewDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Get the ReviewForm view."""
        view = ReviewForm.as_view()
        return view(request, *args, **kwargs)


class BulkReviewsView(MessageMixin, TemplateView):
    """View used to handle bulk reviews."""

    initial: List[dict] = []
    success_url: Optional[str] = None
    prefix: Optional[str] = None
    template_name = "model_reviews/bulk.html"
    formset_invalid_message = _(REVIEW_FORMSET_FAIL_MSG)
    formset_valid_message = _(REVIEW_FORMSET_SUCCESS_MSG)

    def get_initial(self):
        """Return a copy of the initial data to use for formsets on this view."""
        return self.initial[:]

    def get_prefix(self):
        """Return the prefix to use for forms."""
        return self.prefix

    def get_formset_class(self):
        """Get formset."""
        return get_review_formset(user=self.request.user)

    def get_formset(self, formset_class=None):
        """Return an instance of the formset to be used in this view."""
        if formset_class is None:
            formset_class = self.get_formset_class()
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        """Return the keyword arguments for instantiating the formset."""
        kwargs = {
            "initial": self.get_initial(),
            "prefix": self.get_prefix(),
        }

        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }  # flake8: noqa
            )
        return kwargs

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            return self.request.get_full_path()
        return str(self.success_url)  # success_url may be lazy

    def get_context_data(self, **kwargs):
        """Insert the formset into the context dict."""
        if "formset" not in kwargs:
            kwargs["formset"] = self.get_formset()
        return super().get_context_data(**kwargs)

    def formset_valid(self, formset):  # pylint: disable=unused-argument
        """If the form is valid, redirect to the supplied URL."""
        for form in formset:
            if form.has_changed():
                form.save()
        self.messages.success(self.formset_valid_message, fail_silently=True)
        return HttpResponseRedirect(self.get_success_url())

    def formset_invalid(self, formset):
        """If the form is invalid, render the invalid form."""
        self.messages.error(self.formset_invalid_message, fail_silently=True)
        return self.render_to_response(self.get_context_data(formset=formset))

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Handle POST requests.

        Instantiate a form instance with the passed POST variables and then
        check if it's valid.
        """
        formset = self.get_formset()
        if formset.is_valid():
            return self.formset_valid(formset)
        return self.formset_invalid(formset)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        """Handle PUT requests."""
        return self.post(*args, **kwargs)

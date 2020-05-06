"""apps module for model reviews."""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ModelReviewsConfig(AppConfig):
    """App config for model reviews."""

    name = "model_reviews"
    app_label = "model_reviews"
    verbose_name = _("Model Reviews")

    def ready(self):
        """Do stuff when the app is ready."""
        # set up app settings
        # pylint: disable=import-outside-toplevel
        from django.conf import settings
        import approvals.settings as defaults

        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                setattr(settings, name, getattr(defaults, name))

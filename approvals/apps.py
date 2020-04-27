"""apps module for approvals."""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ApprovalsConfig(AppConfig):
    """App config for approvals."""

    name = "approvals"
    app_label = "approvals"
    verbose_name = _("Approvals")

    def ready(self):
        """
        Do stuff when the app is ready
        """
        # set up app settings
        # pylint: disable=import-outside-toplevel
        from django.conf import settings
        import approvals.settings as defaults

        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                setattr(settings, name, getattr(defaults, name))

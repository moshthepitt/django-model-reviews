"""Main init file for django-approvals."""
VERSION = (0, 0, 1)
__version__ = ".".join(str(v) for v in VERSION)
# pylint: disable=invalid-name
default_app_config = "approvals.apps.ModelReviewsConfig"  # noqa

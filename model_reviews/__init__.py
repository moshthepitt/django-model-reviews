"""Main init file for django-model-reviews."""
VERSION = (1, 0, 1)
__version__ = ".".join(str(v) for v in VERSION)
# pylint: disable=invalid-name
default_app_config = "model_reviews.apps.ModelReviewsConfig"  # noqa

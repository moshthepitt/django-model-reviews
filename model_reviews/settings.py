"""Settings module for model reviews."""
MODELREVIEW_FORM_STATUS_FIELD_LABEL = "Status"
MODELREVIEW_FORM_REASON_FIELD_LABEL = "Reason"
MODELREVIEW_FORM_COMMENTS_FIELD_LABEL = "Comments"
MODELREVIEW_PROCESS_REVIEW_FUNCTION = "model_reviews.utils.process_review"
MODELREVIEW_PROCESS_AFTER_SAVE_FUNCTION = (
    "model_reviews.signals.modelreview_after_save_func"
)

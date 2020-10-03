"""Constants module."""
USER = "user"
SANDBOX_FIELD = "_sandbox"
REVIEW_REQUEST_EMAIL_TXT = "There has been a new request that needs your attention."
REVIEW_REQUEST_EMAIL_SUBJ = "New Request For Approval"
REVIEW_COMPLETE_EMAIL_TXT = (
    "Your request has been processed, please log in to view the status."
)
REVIEW_COMPLETE_EMAIL_SUBJ = "Your request has been processed"
EMAIL_TEMPLATE = "generic"
EMAIL_TEMPLATE_PATH = "model_reviews/email"
REVIEW_FORM_SUCCESS_MSG = "Saved successfully. :)"
REVIEW_FORM_FAIL_MSG = "Please correct the errors on the form."
REVIEW_FORMSET_SUCCESS_MSG = REVIEW_FORM_SUCCESS_MSG
REVIEW_FORMSET_FAIL_MSG = "Something went wrong, please try again."
REVIEW_FORM_WRONG_REVIEW_MSG = "Please ensure that you are reviewing the correct item."
REVIEW_FORM_WRONG_REVIEWER_MSG = REVIEW_FORM_WRONG_REVIEW_MSG
REVIEW_FORM_WRONG_STATUS_MSG = "Please submit an approval or rejection."

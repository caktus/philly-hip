from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from wagtail.documents.forms import BaseDocumentForm

from apps.common.utils import is_sso_user

from .utils import scan_pdf_for_malicious_content


class ValidateFileTypeForm(BaseDocumentForm):
    """
    Custom form so that we validate file type BEFORE file gets added to Document Repository.
    """

    def clean_file(self):
        uploaded_file = self.cleaned_data["file"]
        if uploaded_file and "file" in self.changed_data:
            # Only validate the file type if a file made it through previous validation
            # AND if it has changed
            content_type = uploaded_file.content_type
            extension = content_type.split("/")[1]
            if extension.lower() not in settings.WAGTAILDOCS_EXTENSIONS:
                raise forms.ValidationError(
                    f"Only files with these extensions are allowed: {settings.WAGTAILDOCS_EXTENSIONS}. Your file had this type: {content_type}."
                )

            # If the file is a PDF, then scan it to verify that it does not have
            # malicious content.
            if extension.lower() == "pdf":
                try:
                    scan_pdf_for_malicious_content(uploaded_file.temporary_file_path())
                except Exception as error:
                    raise forms.ValidationError(error)
            return uploaded_file


class HIPAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        """SSO users are not allowed to login using the HIPAuthenticationForm."""
        # Run the AuthenticationForm's confirmation checks.
        super().confirm_login_allowed(user)
        # Raise an error if the user is an SSO user.
        if is_sso_user(user):
            raise ValidationError(
                "Users with a Single Sign On (SSO) account must log in via SSO.",
            )

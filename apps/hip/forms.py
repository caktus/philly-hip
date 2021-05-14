from django import forms
from django.conf import settings

from wagtail.documents.forms import BaseDocumentForm

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

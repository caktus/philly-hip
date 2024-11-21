import os

from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile

import pytest
from wagtail.documents import get_document_model
from wagtail.documents.forms import get_document_form

from apps.hip.forms import HIPAuthenticationForm
from apps.hip.tests.factories import DocumentFactory
from apps.users.tests.factories import UserFactory


TESTDATA_DIR = os.path.join(os.path.dirname(__file__), "testdata")


Document = get_document_model()
DocumentForm = get_document_form(Document)


def test_file_is_required(db):
    data = {
        "title": "foo",
    }
    form = DocumentForm(data=data, files={})
    assert not form.is_valid()
    assert "file" in form.errors
    assert form.errors["file"] == ["This field is required."]


def test_pdf_success(db):
    pdf_file_path = os.path.join(TESTDATA_DIR, "test.pdf")
    with open(pdf_file_path, "rb") as pdf_file:
        uploaded_file = TemporaryUploadedFile(
            pdf_file_path, "application/pdf", 1, "utf-8"
        )
        uploaded_file.write(pdf_file.read())
        pdf_file.seek(0)
        data = {"title": "Test Document"}
        form = DocumentForm(data=data, files={"file": uploaded_file})
        assert form.is_valid()


def test_jpeg_success(db):
    f = SimpleUploadedFile("fake.jpeg", b"fake data", content_type="image/jpeg")
    data = {
        "title": "foo",
    }
    form = DocumentForm(data=data, files={"file": f})
    assert form.is_valid()


def test_jpg_success(db):
    f = SimpleUploadedFile("fake.jpg", b"fake data", content_type="image/jpeg")
    data = {
        "title": "foo",
    }
    form = DocumentForm(data=data, files={"file": f})
    assert form.is_valid()


def test_png_success(db):
    f = SimpleUploadedFile("fake.png", b"fake data", content_type="image/png")
    data = {
        "title": "foo",
    }
    form = DocumentForm(data=data, files={"file": f})
    assert form.is_valid()


def test_gif_failure(db):
    f = SimpleUploadedFile("fake.gif", b"fake data", content_type="image/gif")
    data = {
        "title": "foo",
    }
    form = DocumentForm(data=data, files={"file": f})
    assert not form.is_valid()
    assert "Only files with these extensions are allowed" in form.errors["file"][0]


def test_only_pdfs_are_scaned(db, mocker):
    """PDF files are scanned with scan_pdf_for_malicious_content(); non-PDF files are not."""
    # Mock the scan_pdf_for_malicious_content() function to verify that it gets called.
    mock_scan_function = mocker.patch("apps.hip.forms.scan_pdf_for_malicious_content")

    # Uploading a non-PDF file does not call scan_pdf_for_malicious_content()
    for extension, content_type in [
        ("png", "image/png"),
        ("jpg", "image/jpeg"),
        ("jpeg", "image/jpeg"),
    ]:
        uploaded_file = TemporaryUploadedFile(
            f"fake.{extension}", content_type, 1, "utf-8"
        )
        data = {"title": "fake document"}
        form = DocumentForm(data=data, files={"file": uploaded_file})
        assert form.is_valid()
        # The apps.hip.forms.scan_pdf_for_malicious_content() function was not called.
        assert mock_scan_function.called is False

    # Uploading a PDF file calls the apps.hip.forms.scan_pdf_for_malicious_content() function.
    pdf_file_path = os.path.join(TESTDATA_DIR, "test.pdf")
    with open(pdf_file_path, "rb") as pdf_file:
        uploaded_file = TemporaryUploadedFile(
            pdf_file_path, "application/pdf", 1, "utf-8"
        )
        uploaded_file.write(pdf_file.read())
        pdf_file.seek(0)
        data = {"title": "Test Document"}
        form = DocumentForm(data=data, files={"file": uploaded_file})
        assert form.is_valid()
        # The apps.hip.forms.scan_pdf_for_malicious_content() function was called.
        assert mock_scan_function.called is True


def test_edit_document_without_changing_file_success(db):
    document = DocumentFactory()
    data = {
        "title": "new title",
    }
    form = DocumentForm(instance=document, data=data, files={})
    assert form.is_valid()


def test_edit_document_when_changing_file_fails_if_file_is_wrong_type(db):
    document = DocumentFactory()
    f = SimpleUploadedFile("fake.gif", b"fake data", content_type="image/gif")
    data = {
        "title": "new title",
    }
    form = DocumentForm(instance=document, data=data, files={"file": f})
    assert not form.is_valid()
    assert "Only files with these extensions are allowed" in form.errors["file"][0]


@pytest.mark.parametrize(
    "is_sso_user,expected_validity",
    [
        (True, False),
        (False, True),
    ],
)
def test_hip_authentication_form_sso_user(db, mocker, is_sso_user, expected_validity):
    """Only non-SSO users' data is valid for the HIPAuthenticationForm."""
    # Mock the is_sso_user() function.
    mock_is_sso_user = mocker.patch("apps.hip.forms.is_sso_user")
    mock_is_sso_user.return_value = is_sso_user

    # Instantiate the HIPAuthenticationForm form.
    user = UserFactory(password="testpassword1")
    form = HIPAuthenticationForm(
        data={"username": user.email, "password": "testpassword1"}
    )

    # If the user is an SSO user, then the user is not allowed to login.
    if expected_validity:
        assert form.is_valid() is True
    else:
        assert form.is_valid() is False
        expected_error = (
            "Users with a Single Sign On (SSO) account must log in via SSO."
        )
        assert [expected_error] == [error for error in form.errors["__all__"]]
    # The mock_is_sso_user was called.
    assert mock_is_sso_user.called is True

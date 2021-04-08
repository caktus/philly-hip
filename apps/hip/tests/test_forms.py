from django.core.files.uploadedfile import SimpleUploadedFile

from wagtail.documents import get_document_model
from wagtail.documents.forms import get_document_form

from apps.hip.tests.factories import DocumentFactory


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
    f = SimpleUploadedFile("fake.pdf", b"fake data", content_type="application/pdf")
    data = {
        "title": "foo",
    }
    form = DocumentForm(data=data, files={"file": f})
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

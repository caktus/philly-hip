import os

from django.utils.timezone import now, timedelta

import pytest
from wagtail.models import Page

from ..utils import get_most_recent_objects, scan_pdf_for_malicious_content
from .factories import HomePageFactory, StaticPageFactory


TESTDATA_DIR = os.path.join(os.path.dirname(__file__), "testdata")


@pytest.fixture
def pdfid_scan_results_valid():
    """Return the scan results for a valid PDF."""
    return dict(
        reports=[
            {
                "version": "0.2.7",
                "filename": "/temporary_file_path/for/this/file.pdf",
                "header": "%PDF-1.4",
                "obj": 5948,
                "endobj": 5948,
                "stream": 2871,
                "endstream": 2871,
                "xref": 2,
                "trailer": 2,
                "startxref": 2,
                "/Page": 88,
                "/Encrypt": 0,
                "/ObjStm": 171,
                "/JS": 0,
                "/JavaScript": 0,
                "/AA": 0,
                "/OpenAction": 0,
                "/AcroForm": 0,
                "/JBIG2Decode": 0,
                "/RichMedia": 0,
                "/Launch": 0,
                "/EmbeddedFile": 0,
                "/XFA": 0,
                "/Colors > 2^24": 0,
            }
        ]
    )


def test_get_most_recent_objects_zero(db):
    """Calling get_most_recent_objects() for object_count==0 returns an empty list."""
    assert [] == get_most_recent_objects(object_count=0)


def test_get_most_recent_objects_pages_draft_excluded(db):
    """Calling get_most_recent_objects() returns only live Pages."""
    datetime_now = now()

    # Some live pages
    live_pages = [
        HomePageFactory(latest_revision_created_at=now()),
        StaticPageFactory(latest_revision_created_at=now()),
    ]

    # Some draft pages.
    draft_pages = [
        HomePageFactory(latest_revision_created_at=now(), live=False),
        StaticPageFactory(latest_revision_created_at=now(), live=False),
    ]

    # The results only include live (non-draft) Pages.
    results = get_most_recent_objects()
    assert len(live_pages) == len(results)
    for page in live_pages:
        assert page.page_ptr in results
    for page in draft_pages:
        assert page.page_ptr not in results


def test_get_most_recent_objects_pages_correct_order(db):
    """Calling get_most_recent_objects() returns Pages in correct order."""
    datetime_now = now()
    datetime_yesterday = datetime_now - timedelta(days=1)

    home_page_1hr_ago = HomePageFactory(
        latest_revision_created_at=datetime_now - timedelta(hours=1)
    )
    static_page_today = StaticPageFactory(latest_revision_created_at=datetime_now)
    static_page_yesterday = StaticPageFactory(
        latest_revision_created_at=datetime_yesterday
    )

    expected_results = [
        static_page_today.page_ptr,
        home_page_1hr_ago.page_ptr,
        static_page_yesterday.page_ptr,
    ]
    assert expected_results == get_most_recent_objects()


def test_get_most_recent_objects_different_objects_correct_order(db):
    """Calling get_most_recent_objects() returns objects in correct order."""
    datetime_now = now()
    datetime_yesterday = datetime_now - timedelta(days=1)

    home_page_2hr_ago = HomePageFactory(
        latest_revision_created_at=datetime_now - timedelta(hours=2)
    )
    static_page_now = StaticPageFactory(latest_revision_created_at=datetime_now)
    static_page_yesterday = StaticPageFactory(
        latest_revision_created_at=datetime_yesterday
    )

    expected_results = [
        static_page_now.page_ptr,
        home_page_2hr_ago.page_ptr,
        static_page_yesterday.page_ptr,
    ]
    assert expected_results == get_most_recent_objects()


def test_get_most_recent_objects_if_more_objects_than_our_object_count(db):
    """If we have a lot of objects, then make sure we don't truncate our lists before ordering them."""
    datetime_now = now()
    datetime_yesterday = datetime_now - timedelta(days=1)

    home_page_2hr_ago = HomePageFactory(
        latest_revision_created_at=datetime_now - timedelta(hours=2)
    )
    static_page_now = StaticPageFactory(latest_revision_created_at=datetime_now)
    static_page_yesterday = StaticPageFactory(
        latest_revision_created_at=datetime_yesterday
    )

    # we're only going to ask for 1 object, so expect 1 result
    expected_results = [
        static_page_now.page_ptr,
    ]
    assert expected_results == get_most_recent_objects(object_count=1)


def test_get_most_recent_objects_annotations_pages(db):
    """
    Calling get_most_recent_objects() returns objects with annotated fields.

    Each object should have the following fields:
     - name
     - updated_at
     - type_of_object
     - model_name
    """
    home_page = HomePageFactory()
    static_page = StaticPageFactory()

    results = get_most_recent_objects()

    for result in results:
        assert result.name == result.title
        assert result.updated_at == result.latest_revision_created_at
        assert result.type_of_object == "PAGE"
        assert result.model_name == "page"


def test_get_most_recent_objects_pages_parameter(db):
    """Passing a 'pages_qs' parameter means most recent Pages come from only those Pages."""
    datetime_now = now()
    datetime_yesterday = datetime_now - timedelta(days=1)

    home_page_2hr_ago = HomePageFactory(
        latest_revision_created_at=datetime_now - timedelta(hours=2)
    )
    static_page_now = StaticPageFactory(latest_revision_created_at=datetime_now)
    static_page_yesterday = StaticPageFactory(
        latest_revision_created_at=datetime_yesterday
    )

    # Passing a 'pages_qs' parameter only returns those Pages, in order of their
    # most recent revision.
    assert [home_page_2hr_ago.page_ptr] == get_most_recent_objects(
        pages_qs=Page.objects.filter(id=home_page_2hr_ago.page_ptr.id)
    )
    assert [static_page_now.page_ptr] == get_most_recent_objects(
        pages_qs=Page.objects.filter(id=static_page_now.page_ptr.id)
    )
    assert [static_page_yesterday.page_ptr] == get_most_recent_objects(
        pages_qs=Page.objects.filter(id=static_page_yesterday.page_ptr.id)
    )
    assert [
        static_page_now.page_ptr,
        home_page_2hr_ago.page_ptr,
    ] == get_most_recent_objects(
        pages_qs=Page.objects.filter(
            id__in=[home_page_2hr_ago.page_ptr.id, static_page_now.page_ptr.id]
        )
    )
    assert [
        static_page_now.page_ptr,
        static_page_yesterday.page_ptr,
    ] == get_most_recent_objects(
        pages_qs=Page.objects.filter(
            id__in=[static_page_now.page_ptr.id, static_page_yesterday.page_ptr.id]
        )
    )
    assert [
        home_page_2hr_ago.page_ptr,
        static_page_yesterday.page_ptr,
    ] == get_most_recent_objects(
        pages_qs=Page.objects.filter(
            id__in=[home_page_2hr_ago.page_ptr.id, static_page_yesterday.page_ptr.id]
        )
    )
    assert [
        static_page_now.page_ptr,
        home_page_2hr_ago.page_ptr,
        static_page_yesterday.page_ptr,
    ] == get_most_recent_objects(
        pages_qs=Page.objects.filter(
            id__in=[
                home_page_2hr_ago.page_ptr.id,
                static_page_now.page_ptr.id,
                static_page_yesterday.page_ptr.id,
            ]
        )
    )


def test_scan_pdf_for_malicious_content_no_file(db):
    """Not passing a file to scan_pdf_for_malicious_content() raises an error."""
    with pytest.raises(Exception) as error:
        scan_pdf_for_malicious_content()


def test_scan_pdf_for_malicious_content_not_pdf(db):
    """Scanning a non-PDF file raises an error."""
    text_file_path = os.path.join(TESTDATA_DIR, "test.txt")
    with pytest.raises(Exception) as error:
        scan_pdf_for_malicious_content(text_file_path)
    assert "Invalid PDF" == str(error.value)


def test_scan_pdf_for_malicious_content_zero_pages(
    db, mocker, pdfid_scan_results_valid
):
    """Scanning a PDF file with 0 pages raises an error."""
    # Mock the pdfid.PDFiDMain() method to return a result with 0 pages.
    mock_scan_results = mocker.patch("apps.hip.utils.pdfid")
    pdfid_scan_results_valid["reports"][0]["/Page"] = 0
    mock_scan_results.PDFiDMain.return_value = pdfid_scan_results_valid

    pdf_file_path = os.path.join(TESTDATA_DIR, "test.pdf")
    with pytest.raises(Exception) as error:
        scan_pdf_for_malicious_content(pdf_file_path)
    assert "Invalid PDF" == str(error.value)


def test_scan_pdf_for_malicious_content_open_or_auto_action_no_js(
    db, mocker, pdfid_scan_results_valid
):
    """Scanning a PDF file that has an open or automatic action, with no JS, is ok."""
    # Mock the pdfid.PDFiDMain() method to return a result with 1 open action and
    # 1 automatic action, but no JavaScript.
    mock_scan_results = mocker.patch("apps.hip.utils.pdfid")
    results_open_actions = pdfid_scan_results_valid.copy()
    results_open_actions["reports"][0]["/OpenAction"] = 1
    results_open_actions["reports"][0]["/AA"] = 1
    results_open_actions["reports"][0]["/JS"] = 0
    results_open_actions["reports"][0]["/JavaScript"] = 0
    mock_scan_results.PDFiDMain.return_value = results_open_actions

    pdf_file_path = os.path.join(TESTDATA_DIR, "test.pdf")
    # Scanning the PDF file does not raise any errors.
    scan_pdf_for_malicious_content(pdf_file_path)


@pytest.mark.parametrize(
    "scan_results_js_javascript", [(1, 0), (0, 1), (1, 1), (2, 25)]
)
def test_scan_pdf_for_malicious_content_open_or_auto_action_with_js(
    db, mocker, pdfid_scan_results_valid, scan_results_js_javascript
):
    """Scanning a PDF file that has an open or automatic action, with JS, raises an error."""
    # These are the values for the scan results, determining that the PDF file has
    # some JavaScript. If the file has an open or automatic action along with any
    # JavaScript, then scan_pdf_for_malicious_content() raises an error.
    js_value, javascript_value = scan_results_js_javascript
    # Mock the pdfid.PDFiDMain() method to return a result with 1 open action and
    # 1 automatic action, with JavaScript.
    mock_scan_results = mocker.patch("apps.hip.utils.pdfid")
    results_open_actions = pdfid_scan_results_valid.copy()
    results_open_actions["reports"][0]["/OpenAction"] = 1
    results_open_actions["reports"][0]["/AA"] = 1
    results_open_actions["reports"][0]["/JS"] = js_value
    results_open_actions["reports"][0]["/JavaScript"] = javascript_value
    mock_scan_results.PDFiDMain.return_value = results_open_actions

    pdf_file_path = os.path.join(TESTDATA_DIR, "test.pdf")
    with pytest.raises(Exception) as error:
        scan_pdf_for_malicious_content(pdf_file_path)
    assert "This PDF file has suspicious content." == str(error.value)


def test_scan_pdf_for_malicious_content_javascript_no_open_or_automatic_action(
    db, mocker, pdfid_scan_results_valid
):
    """Scanning a PDF file that has JavaScript, but no open action or automatic action is ok."""
    # Mock the pdfid.PDFiDMain() method to return a result with 0 open action and
    # 0 automatic action, but some JavaScript.
    mock_scan_results = mocker.patch("apps.hip.utils.pdfid")
    results_open_actions = pdfid_scan_results_valid.copy()
    results_open_actions["reports"][0]["/OpenAction"] = 0
    results_open_actions["reports"][0]["/AA"] = 0
    results_open_actions["reports"][0]["/JS"] = 100
    results_open_actions["reports"][0]["/JavaScript"] = 123
    mock_scan_results.PDFiDMain.return_value = results_open_actions

    pdf_file_path = os.path.join(TESTDATA_DIR, "test.pdf")
    # Scanning the PDF file does not raise any errors.
    scan_pdf_for_malicious_content(pdf_file_path)


def test_scan_pdf_for_malicious_content_valid_pdf(db):
    """Scanning a non-malicious PDF file succeeds."""
    pdf_file_path = os.path.join(TESTDATA_DIR, "test.pdf")
    # Scanning the PDF file does not raise any errors.
    scan_pdf_for_malicious_content(pdf_file_path)

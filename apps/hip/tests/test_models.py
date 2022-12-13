from django.shortcuts import reverse

from wagtail.models import Page

from apps.hip.models import HIPDocument
from apps.hip.tests.factories import DocumentFactory, HomePageFactory, StaticPageFactory


def assert_document_match(expected_documents, search_term):
    """Assert that searching HIPDocuments by the search_term returns expected results."""
    assert list(
        HIPDocument.objects.filter(
            id__in=[document.id for document in expected_documents]
        )
    ) == list(HIPDocument.objects.search(search_term))


def test_homepage_context_recent_updates(db, rf, mocker):
    """The HomePage 'recent_updates' are limited to Pages the request.user can see."""
    home_page = HomePageFactory()
    static_page = StaticPageFactory(parent=home_page, title="Static Page")

    # Mock the apps.common.utils.get_all_pages_visible_to_request function,
    # since it should be used to get the Pages visible to the request.user.
    mock_get_all_pages_visible_to_request = mocker.patch(
        "apps.common.utils.get_all_pages_visible_to_request"
    )
    pages_visible_to_user = Page.objects.filter(id=static_page.id)
    mock_get_all_pages_visible_to_request.return_value = pages_visible_to_user
    # Mock the apps.hip.utils.get_most_recent_objects function, since it should
    # be used to get the most recent Pages.
    mock_get_most_recent_objects = mocker.patch(
        "apps.hip.utils.get_most_recent_objects"
    )

    request = rf.get("/someurl/")

    context = home_page.get_context(request)

    assert mock_get_all_pages_visible_to_request.called
    assert (request,) == mock_get_all_pages_visible_to_request.call_args_list[0][0]
    assert mock_get_most_recent_objects.called
    assert list(pages_visible_to_user) == list(
        mock_get_most_recent_objects.call_args_list[0][1]["pages_qs"]
    )
    assert context["recent_updates"] == mock_get_most_recent_objects.return_value


def test_hipdocument_search_empty_search_term(db):
    """Not having a search term yields no results."""
    DocumentFactory(title="Smallpox Document")

    assert_document_match([], "")
    assert_document_match([], " ")


def test_hipdocument_search_no_matches(db):
    """Searching with a search term that does not match any documents yields no results."""
    DocumentFactory(title="Smallpox Document")

    assert_document_match([], "jfnkjsdnfskjnfsjk")


def test_hipdocument_search_single_term_full_match(db):
    """Searching with a search term that fully matches a document yields that document."""
    document_smallpox = DocumentFactory(title="Smallpox Document")
    DocumentFactory(title="Other Document")

    assert_document_match([document_smallpox], "smallpox")


def test_hipdocument_search_multiple_term_full_match(db):
    """Searching with multiple search terms that fully match a document yields that document."""
    document_smallpox = DocumentFactory(title="Smallpox Document")
    DocumentFactory(title="Other Document")

    assert_document_match([document_smallpox], "smallpox document")


def test_hipdocument_search_partial_term_partial_match(db):
    """Searching with a search term that partially matches a document yields that document."""
    document_smallpox = DocumentFactory(title="Smallpox Document")
    DocumentFactory(title="Other Document")

    assert_document_match([document_smallpox], "pox")


def test_hipdocument_search_partial_term_partial_matches(db):
    """Searching with a search term that partially matches documents yields those documents."""
    document_smallpox = DocumentFactory(title="Smallpox Document")
    document_small_chance = DocumentFactory(title="Small Chance To Be Sick")
    document_another = DocumentFactory(title="Another Document")

    assert_document_match([document_smallpox, document_small_chance], "small")
    assert_document_match(
        [document_small_chance, document_smallpox, document_another], "a"
    )


def test_hipdocument_url_with_file(db):
    """Test the HIPDocument.url property for a HIPDocument with a file."""
    document = DocumentFactory(title="Smallpox Document")
    expected_url = reverse(
        "get_document",
        kwargs={"document_id": document.id, "document_name": document.filename},
    )
    assert expected_url == document.url


def test_hipdocument_url_without_file(db):
    """Test the HIPDocument.url property for a HIPDocument without a file."""
    document_no_file = DocumentFactory(title="Other Document", file=None)
    assert "" == document_no_file.url

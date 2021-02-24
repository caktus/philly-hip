from django.utils.timezone import now, timedelta

from wagtail_factories.factories import DocumentFactory

from ..utils import get_most_recent_objects
from .factories import HomePageFactory, StaticPageFactory


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


def test_get_most_recent_objects_documents_correct_order(db):
    """Calling get_most_recent_objects() returns Documents in correct order."""
    datetime_now = now()
    datetime_yesterday = datetime_now - timedelta(days=1)

    document_1hr_ago = DocumentFactory()
    document_1hr_ago.created_at = datetime_now - timedelta(hours=1)
    document_1hr_ago.save()
    document_now = DocumentFactory()
    document_now.created_at = datetime_now
    document_now.save()
    document_yesterday = DocumentFactory()
    document_yesterday.created_at = datetime_yesterday
    document_yesterday.save()

    expected_results = [document_now, document_1hr_ago, document_yesterday]
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

    document_1hr_ago = DocumentFactory()
    document_1hr_ago.created_at = datetime_now - timedelta(hours=1)
    document_1hr_ago.save()

    expected_results = [
        static_page_now.page_ptr,
        document_1hr_ago,
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

    document_1hr_ago = DocumentFactory()
    document_1hr_ago.created_at = datetime_now - timedelta(hours=1)
    document_1hr_ago.save()

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


def test_get_most_recent_objects_annotations_documents(db):
    """
    Calling get_most_recent_objects() returns objects with annotated fields.

    Each object should have the following fields:
     - name
     - updated_at
     - type_of_object
     - model_name
    """
    document = DocumentFactory(file="example.pdf")

    results = get_most_recent_objects()

    assert results[0].name == document.title
    assert results[0].updated_at == document.created_at
    assert results[0].type_of_object == document.file.name.split(".")[-1].upper()
    assert results[0].model_name == "document"

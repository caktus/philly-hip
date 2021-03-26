from django.contrib.auth.models import AnonymousUser, Group

import pytest
from wagtail.core.models import Page, PageViewRestriction

from apps.auth_content.tests.factories import ClosedPODHomePageFactory
from apps.users.tests.factories import UserFactory

from ..context_processors import authenticated_home_pages, previous_url


@pytest.fixture
def closedpod_homepage():
    """Create a ClosedPODHomePage as a child of the homepage."""
    # The current home page of the site.
    homepage = (
        Page.objects.all().filter(title="Welcome to your new Wagtail site!").first()
    )
    homepage.url_path = "/"
    homepage.save()
    # Create a ClosedPODHomePage
    closedpodhomepage = ClosedPODHomePageFactory(parent=homepage)
    # The ClosedPODHomePage is restricted to users in the "Closed POD" Group.
    page_view_restriction = PageViewRestriction.objects.create(
        page=closedpodhomepage, restriction_type="groups"
    )
    group_closedpod = Group.objects.get(name="Closed POD")
    page_view_restriction.groups.add(group_closedpod)

    return closedpodhomepage


def test_previous_url_with_http_referrer(db, rf, mocker):
    """If the request has an HTTP_REFERER, its value is the previous_url."""
    # Mock the apps.common.utils.get_home_page_url function to verify that it
    # does not get called.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_url

    request = rf.get("/someurl")
    referrer_url = "https://example.com"
    request.META["HTTP_REFERER"] = referrer_url

    assert {"previous_url": referrer_url} == previous_url(request)
    # The get_home_page_url() function was not called.
    assert mock_get_home_page_url.called is False


def test_previous_url_with_empty_http_referrer(db, rf, mocker):
    """If the request has an empty HTTP_REFERER, its value is the previous_url."""
    # Mock the apps.common.utils.get_home_page_url function to verify that it
    # does not get called.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_url

    request = rf.get("/someurl")
    referrer_url = ""
    request.META["HTTP_REFERER"] = referrer_url

    assert {"previous_url": referrer_url} == previous_url(request)
    # The get_home_page_url() function was not called.
    assert mock_get_home_page_url.called is False


def test_previous_url_no_http_referrer(db, rf, mocker):
    """If the request has no HTTP_REFERER, previous_url is value of get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url() function.
    mock_get_home_page_url = mocker.patch(
        "apps.common.context_processors.get_home_page_url"
    )
    mock_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_url

    request = rf.get("/someurl")

    assert {"previous_url": mock_url} == previous_url(request)
    assert 1 == mock_get_home_page_url.call_count


def test_authenticated_home_pages_not_authenticated(db, rf, closedpod_homepage):
    """A user who is not authenticated may not see any authenticated home pages."""
    # Create a user who is not in any Groups, and is not authenticated.
    request = rf.get("/someurl")
    request.user = AnonymousUser()
    assert request.user.is_authenticated is False

    assert {"authenticated_home_pages": []} == authenticated_home_pages(request)


def test_authenticated_home_pages_authenticated_not_authorized(
    db, rf, closedpod_homepage
):
    """
    A user who is authenticated, but not authorized, may not see any authenticated home pages.

    In order to see the ClosedPODHomePage, a user must be in the "Closed POD" Group.
    """
    # Create a user who is not in any Groups, but is authenticated.
    request = rf.get("/someurl")
    user = UserFactory()
    user.groups.clear()
    request.user = user
    assert request.user.is_authenticated

    assert {"authenticated_home_pages": []} == authenticated_home_pages(request)


def test_authenticated_home_pages_no_authenticated_homepages(db, rf):
    """If no authenticated home pages exist, then they may not be viewed."""
    request = rf.get("/someurl")

    # Create a user who is in the "Closed POD" Group, and is authenticated.
    user = UserFactory()
    group_closedpod = Group.objects.get(name="Closed POD")
    user.groups.add(group_closedpod)
    request.user = user
    assert request.user.is_authenticated

    # Even though the request.user has permission to see the ClosedPODHomePage,
    # the page does not exist, so the request.user may not see it.
    assert {"authenticated_home_pages": []} == authenticated_home_pages(request)


def test_authenticated_home_pages_authenticated_and_authorized(
    db, rf, closedpod_homepage
):
    """
    A user who is authenticated and authorized may see any authenticated home pages.

    In order to see the ClosedPODHomePage, a user must be in the "Closed POD" Group.
    """
    request = rf.get("/someurl")
    # Create a user who is in the "Closed POD" Group, and is authenticated.
    user = UserFactory()
    group_closedpod = Group.objects.get(name="Closed POD")
    user.groups.add(group_closedpod)
    request.user = user
    assert request.user.is_authenticated

    # The request.user is allowed to see the Closed POD homepage.
    expected_results = {
        "authenticated_home_pages": [
            {"name": "Closed POD Home", "url": closedpod_homepage.url},
        ]
    }
    assert expected_results == authenticated_home_pages(request)

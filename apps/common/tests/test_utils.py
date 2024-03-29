import random

from django.contrib.auth.models import AnonymousUser, Group

import pytest
from social_django.models import UserSocialAuth
from wagtail.models import Page

from apps.auth_content.tests.factories import (
    BigCitiesHomePageFactory,
    ClosedPODHomePageFactory,
    PCWMSAHomePageFactory,
)
from apps.hip.tests.factories import HomePageFactory, StaticPageFactory
from apps.users.tests.factories import UserFactory

from ..utils import (
    closedpod_user_check,
    get_all_pages_visible_to_request,
    get_bigcities_home_page_url,
    get_closedpod_home_page_url,
    get_emergency_communications_page_url,
    get_home_page_url,
    get_next_url_from_request,
    get_pcwmsa_home_page_url,
    is_sso_user,
)


def test_get_home_page_url_no_homepage(db):
    """If no HomePage exists, then the function returns '/'."""
    assert "/" == get_home_page_url()


def test_get_home_page_url_no_live_homepage(db):
    """If no live HomePage exists, then the function returns '/'."""
    # Delete any Pages with a URL path of "/".
    Page.objects.all().filter(url_path="/").delete()

    home_page = HomePageFactory(live=False, url_path="/")
    assert "/" == get_home_page_url()
    assert home_page.url != get_home_page_url()


def test_get_home_page_url_with_homepage(db):
    """If a live HomePage exists, then the function returns its URL."""
    home_page = HomePageFactory(live=True, url_path="/")
    assert home_page.url == get_home_page_url()


def test_get_closedpod_home_page_url_no_closedpod_homepage(db, mocker):
    """If no ClosedPODHomePage exists, then the function returns get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url

    assert mock_homepage_url == get_closedpod_home_page_url()


def test_get_closedpod_home_page_url_no_live_homepage(db, mocker):
    """If no live ClosedPODHomePage exists, then the function returns get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url

    closedpod_home_page = ClosedPODHomePageFactory(live=False)
    assert mock_homepage_url == get_closedpod_home_page_url()
    assert closedpod_home_page.url != get_closedpod_home_page_url()


def test_get_closedpod_home_page_url_with_closedpod_homepage(db, mocker):
    """If a live ClosedPODHomePage exists, then the function returns its URL."""
    closedpod_home_page = ClosedPODHomePageFactory(live=True)
    assert closedpod_home_page.url == get_closedpod_home_page_url()


def test_get_pcwmsa_home_page_url_no_pcwmsa_homepage(db, mocker):
    """If no PCWMSAHomePage exists, then the function returns get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url

    assert mock_homepage_url == get_pcwmsa_home_page_url()


def test_get_pcwmsa_home_page_url_no_live_homepage(db, mocker):
    """If no live PCWMSAHomePage exists, then the function returns get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url

    pcwmsa_home_page = PCWMSAHomePageFactory(live=False)
    assert mock_homepage_url == get_pcwmsa_home_page_url()
    assert pcwmsa_home_page.url != get_pcwmsa_home_page_url()


def test_get_pcwmsa_home_page_url_with_pcwmsa_homepage(db, mocker):
    """If a live PCWMSAHomePage exists, then the function returns its URL."""
    pcwmsa_home_page = PCWMSAHomePageFactory(live=True)
    assert pcwmsa_home_page.url == get_pcwmsa_home_page_url()


def test_get_bigcities_home_page_url_no_bigcities_homepage(db, mocker):
    """If no BigCitiesHomePage exists, then the function returns get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url

    assert mock_homepage_url == get_bigcities_home_page_url()


def test_get_bigcities_home_page_url_no_live_homepage(db, mocker):
    """If no live BigCitiesHomePage exists, then the function returns get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url

    bigcities_home_page = BigCitiesHomePageFactory(live=False)
    assert mock_homepage_url == get_bigcities_home_page_url()
    assert bigcities_home_page.url != get_bigcities_home_page_url()


def test_get_bigcities_home_page_url_with_bigcities_homepage(db, mocker):
    """If a live BigCitiesHomePage exists, then the function returns its URL."""
    bigcities_home_page = BigCitiesHomePageFactory(live=True)
    assert bigcities_home_page.url == get_bigcities_home_page_url()


def test_get_emergency_communications_page_url_no_emergency_communications_page(
    db, mocker
):
    """If no "Emergency Communications" Page exists, then function returns get_home_page_url()."""
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url

    assert mock_homepage_url == get_emergency_communications_page_url()


def test_get_emergency_communications_page_url_no_live_emergency_communications_page(
    db, mocker
):
    """
    If no live "Emergency Communications" Page exists, then function returns get_home_page_url().
    """
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.common.utils.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url
    # Create an "Emergency Communications" page that is not live.
    emergency_communications_page = StaticPageFactory(
        title="Emergency Communications", live=False
    )

    assert mock_homepage_url == get_emergency_communications_page_url()
    assert emergency_communications_page.url != get_emergency_communications_page_url()


def test_get_emergency_communications_page_url_with_emergency_communications_page(
    db, mocker
):
    """If a live "Emergency Communications" Page exists, then the function returns its URL."""
    emergency_communications_page = StaticPageFactory(
        title="Emergency Communications", live=True
    )
    assert emergency_communications_page.url == get_emergency_communications_page_url()


def test_get_all_pages_visible_to_request_unauthenticated(
    db,
    rf,
    bigcities_homepage_with_descendants,  # noqa: F811
    closedpod_homepage_with_descendants,  # noqa: F811
    pcwmsa_homepage_with_descendants,  # noqa: F811
    public_pages_with_descendants,  # noqa: F811
):
    """Test get_all_pages_visible_to_request() for an unauthenticated user."""
    # A request with an anonymous user.
    request = rf.get("/someurl/")
    request.user = AnonymousUser()
    # The expected results are the public pages.
    expected_results = public_pages_with_descendants

    results = get_all_pages_visible_to_request(request)

    assert len(expected_results) == len(results)
    for expected_result in expected_results:
        assert expected_result in results


def test_get_all_pages_visible_to_request_authenticated_not_in_groups(
    db,
    rf,
    bigcities_homepage_with_descendants,  # noqa: F811
    closedpod_homepage_with_descendants,  # noqa: F811
    pcwmsa_homepage_with_descendants,  # noqa: F811
    public_pages_with_descendants,  # noqa: F811
):
    """Test get_all_pages_visible_to_request() for an authenticated user not in any Groups."""
    # A request with a user, who is not in any Groups.
    request = rf.get("/someurl/")
    user = UserFactory(email="test@example.com")
    assert not user.groups.exists()
    request.user = user
    # Because the request.user is not in any Groups, the request.user is not able
    # to see any of the private Pages, so the expected results are the public pages.
    expected_results = public_pages_with_descendants

    results = get_all_pages_visible_to_request(request)

    assert len(expected_results) == len(results)
    for expected_result in expected_results:
        assert expected_result in results


def test_get_all_pages_visible_to_request_authenticated_superuser_not_in_groups(
    db,
    rf,
    bigcities_homepage_with_descendants,  # noqa: F811
    closedpod_homepage_with_descendants,  # noqa: F811
    pcwmsa_homepage_with_descendants,  # noqa: F811
    public_pages_with_descendants,  # noqa: F811
):
    """Test get_all_pages_visible_to_request() for an authenticated superuser not in any Groups."""
    # A request with a user, who is not in any Groups.
    request = rf.get("/someurl/")
    user = UserFactory(email="test@example.com", is_superuser=True)
    assert not user.groups.exists()
    assert user.is_superuser
    request.user = user
    # Even though the request.user is not in any Groups, because the request.user
    # is a superuser, the request.user is allowed to see all of the Pages.
    expected_results = (
        public_pages_with_descendants
        + bigcities_homepage_with_descendants
        + closedpod_homepage_with_descendants
        + pcwmsa_homepage_with_descendants
    )

    results = get_all_pages_visible_to_request(request)

    assert len(expected_results) == len(results)
    for expected_result in expected_results:
        assert expected_result in results


def test_get_all_pages_visible_to_request_authenticated_adminuser_not_in_groups(
    db,
    rf,
    bigcities_homepage_with_descendants,  # noqa: F811
    closedpod_homepage_with_descendants,  # noqa: F811
    pcwmsa_homepage_with_descendants,  # noqa: F811
    public_pages_with_descendants,  # noqa: F811
):
    """Test get_all_pages_visible_to_request() for an authenticated admin user not in any Groups."""
    # A request with a user, who is not in any Groups.
    request = rf.get("/someurl/")
    user = UserFactory(email="test@example.com")
    user.is_admin = True
    user.save()
    assert not user.groups.exists()
    assert not user.is_superuser
    request.user = user
    # Because the request.user is not in any Groups, the request.user is not able
    # to see any of the private Pages, so the expected results are the public pages.
    expected_results = public_pages_with_descendants

    results = get_all_pages_visible_to_request(request)

    assert len(expected_results) == len(results)
    for expected_result in expected_results:
        assert expected_result in results


@pytest.mark.parametrize(
    "group_names,expected_pages",
    [
        ([], "get_home_page_url"),
        (["Closed POD"], ["closedpod_homepage_with_descendants"]),
        (["PCW MSA"], ["pcwmsa_homepage_with_descendants"]),
        (["Big Cities"], ["bigcities_homepage_with_descendants"]),
        (
            ["Closed POD", "PCW MSA"],
            ["closedpod_homepage_with_descendants", "pcwmsa_homepage_with_descendants"],
        ),
        (
            ["Closed POD", "Big Cities"],
            [
                "closedpod_homepage_with_descendants",
                "bigcities_homepage_with_descendants",
            ],
        ),
        (
            ["PCW MSA", "Big Cities"],
            ["pcwmsa_homepage_with_descendants", "bigcities_homepage_with_descendants"],
        ),
        (
            ["Closed POD", "PCW MSA", "Big Cities"],
            [
                "closedpod_homepage_with_descendants",
                "pcwmsa_homepage_with_descendants",
                "bigcities_homepage_with_descendants",
            ],
        ),
    ],
)
def test_get_all_pages_visible_to_request_authenticated_in_group(
    db,
    rf,
    bigcities_homepage_with_descendants,  # noqa: F811
    closedpod_homepage_with_descendants,  # noqa: F811
    pcwmsa_homepage_with_descendants,  # noqa: F811
    public_pages_with_descendants,  # noqa: F811
    group_names,
    expected_pages,
):
    """Test get_all_pages_visible_to_request() for an authenticated user in Group(s)."""
    # Create a user, and put the user into particular Group(s).
    user = UserFactory(email="test-user")
    for group_name in group_names:
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
    # A request with the user.
    request = rf.get("/someurl/")
    request.user = user
    # Determine the Pages that the user should be allowed to see. The user should
    # be able to see all of the public Pages, as well as any Pages for their Group.
    expected_results = public_pages_with_descendants
    for expected_page_name in expected_pages:
        if expected_page_name == "closedpod_homepage_with_descendants":
            expected_results += closedpod_homepage_with_descendants
        elif expected_page_name == "pcwmsa_homepage_with_descendants":
            expected_results += pcwmsa_homepage_with_descendants
        elif expected_page_name == "bigcities_homepage_with_descendants":
            expected_results += bigcities_homepage_with_descendants

    results = get_all_pages_visible_to_request(request)

    assert len(expected_results) == len(results)
    for expected_result in expected_results:
        assert expected_result in results


def test_closedpod_user_check_anonymoususer(db):
    """An anonymous user is not in the "Closed POD" Group."""
    user = AnonymousUser()
    assert closedpod_user_check(user) is False


def test_closedpod_user_check_no_groups(db):
    """A user who is not in any Groups is not in the "Closed POD" Group."""
    user = UserFactory()
    assert closedpod_user_check(user) is False


def test_closedpod_user_check_wrong_group(db):
    """Test closedpod_user_check() for a user who is in a Group, but not the "Closed POD" Group."""
    user = UserFactory()
    user.groups.add(Group.objects.get(name="PCW MSA"))
    assert closedpod_user_check(user) is False


def test_closedpod_user_check_correct_group(db):
    """Test closedpod_user_check() for a user who is in the "Closed POD" Group."""
    user = UserFactory()
    user.groups.add(Group.objects.get(name="Closed POD"))
    assert closedpod_user_check(user) is True


def test_closedpod_user_check_multiple_groups(db):
    """Test closedpod_user_check() for a user who is in multiple Groups."""
    user = UserFactory()
    user.groups.add(Group.objects.get(name="PCW MSA"))
    user.groups.add(Group.objects.get(name="Closed POD"))
    user.groups.add(Group.objects.get(name="Big Cities"))
    assert closedpod_user_check(user) is True


def test_closedpod_user_check_no_groups_admin_staff(db):
    """A staff user who is not in any Groups is not Closed POD user."""
    user = UserFactory()
    user.is_staff = True
    user.save()
    assert closedpod_user_check(user) is False


def test_closedpod_user_check_no_groups_superuser(db):
    """A superuser who is not in any Groups is a Closed POD user."""
    user = UserFactory()
    user.is_superuser = True
    user.save()
    assert closedpod_user_check(user) is True


@pytest.mark.parametrize(
    "social_auth_exists,philagov_email,is_superuser,is_admin,expected_result",
    [
        (False, False, False, False, False),
        (True, False, False, False, True),  # users with social auth are SSO users
        (False, True, False, False, True),  # users with a phila.gov email are SSO users
        (False, False, True, False, False),
        (False, False, False, True, False),
        (True, True, False, False, True),  # users with social auth are SSO users
        (True, False, True, False, True),  # users with social auth are SSO users
        (True, False, False, True, True),  # users with social auth are SSO users
        (False, True, True, False, True),  # users with a phila.gov email are SSO users
        (False, True, False, True, True),  # users with a phila.gov email are SSO users
        (False, False, True, True, False),
        (True, True, True, False, True),  # users with social auth are SSO users
        (True, True, False, True, True),  # users with social auth are SSO users
        (True, False, True, True, True),  # users with social auth are SSO users
        (False, True, True, True, True),  # users with social auth are SSO users
        (True, True, True, True, True),  # users with social auth are SSO users
    ],
)
def test_is_sso_user(
    db,
    social_auth_exists,
    philagov_email,
    is_superuser,
    is_admin,
    expected_result,
):
    """Test the is_sso_user() utility function."""
    # Set up the test user.
    user = UserFactory()
    if social_auth_exists:
        social_auth_for_user = UserSocialAuth.objects.create(user=user)
    if philagov_email:
        user.email = f"{random.random()}@phila.gov"
    if is_superuser:
        user.is_superuser = True
    if is_admin:
        user.is_staff = True
    user.save()

    # Verify the value of the is_sso_user() utility function for the user.
    assert is_sso_user(user) is expected_result


@pytest.mark.parametrize(
    "next_url,http_referrer_header,expected_url",
    [
        (None, None, None),
        ("", "", None),
        ("/the_next_url/", "", "/the_next_url/"),
        ("", "/the_http_referer_header/", "/the_http_referer_header/"),
        ("/the_next_url/", "/the_http_referer_header/", "/the_next_url/"),
    ],
)
def test_get_next_url_from_request(
    db, rf, next_url, http_referrer_header, expected_url
):
    """Test the get_next_url_from_request() utility function."""
    request_url = "/test_url/"
    if next_url is not None:
        request_url += f"?next={next_url}"
    request = rf.get(request_url, HTTP_REFERER=http_referrer_header)

    result = get_next_url_from_request(request)
    assert expected_url == result

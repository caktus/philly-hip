from django.contrib.auth.models import Group
from django.shortcuts import reverse

import pytest

from apps.users.tests.factories import GroupFactory, UserFactory


def test_hip_login_view_post_remember_user(db, client):
    """Logging in and setting 'remember_me' to True means user is remembered."""
    user = UserFactory(email="test-user")
    user.set_password("testpassword1")
    user.save()

    # Currently, the client session is not set to expire at browser close.
    assert client.session.get_expire_at_browser_close() is False

    response = client.post(
        reverse("login"),
        {"username": user.email, "password": "testpassword1", "remember_me": True},
    )
    # The session is still not set to expire when the browser is closed.
    assert client.session.get_expire_at_browser_close() is False


@pytest.mark.parametrize("remember_me", ["", False, None])
def test_hip_login_view_post_do_not_remember_user(db, client, remember_me):
    """Logging in and setting 'remember_me' to a falsey value means user is not remembered."""
    user = UserFactory(email="test-user")
    user.set_password("testpassword1")
    user.save()

    # Currently, the client session is not set to expire at browser close.
    assert client.session.get_expire_at_browser_close() is False

    post_data = {"username": user.email, "password": "testpassword1"}
    if remember_me is not None:
        post_data["remember_me"] = remember_me
    response = client.post(reverse("login"), post_data)

    # The session is now set to expire when the browser is closed.
    assert client.session.get_expire_at_browser_close() is True


def test_hip_login_view_post_no_next_parameter(db, client):
    """Logging in without a 'next' parameter means user is redirected to auth_view_router."""
    user = UserFactory(email="test-user")
    user.set_password("testpassword1")
    user.save()

    response = client.post(
        reverse("login"),
        {"username": user.email, "password": "testpassword1", "remember_me": True},
    )

    # The user is redirected to auth_view_router
    assert 302 == response.status_code
    assert reverse("auth_view_router") == response.url


def test_hip_login_view_post_with_next_parameter(db, client):
    """Logging in with a 'next' parameter means user is redirected to that parameter."""
    user = UserFactory(email="test-user")
    user.set_password("testpassword1")
    user.save()

    response = client.post(
        f"{reverse('login')}?next=next_page",
        {"username": user.email, "password": "testpassword1", "remember_me": True},
    )

    # The user is redirected to auth_view_router
    assert 302 == response.status_code
    assert "next_page" == response.url


def test_hip_login_view_get_unauthenticated(db, client):
    """An unauthenticated user GETting the login page sees the login page."""
    response = client.get(reverse("login"))
    assert 200 == response.status_code
    assert ["registration/login.html"] == response.template_name


def test_hip_login_view_get_authenticated(db, client):
    """An authenticated user GETting the login page is redirected to the auth_view_router."""
    # Log in the user.
    user = UserFactory(email="test-user")
    client.force_login(user)

    response = client.get(reverse("login"))

    # GETting the login page redirects the user to the auth_view_router view.
    assert 302 == response.status_code
    assert reverse("auth_view_router") == response.url


def test_authenticated_view_router_not_authenticated(db, client, mocker):
    """Unauthenticated users do not have access to the authenticated_view_router."""
    # Mock the apps.common.utils.get_home_page_url function, to verify it does
    # not get called.
    mock_get_home_page_url = mocker.patch("apps.hip.views.get_home_page_url")

    # A user is not logged in.
    client.logout()

    response = client.get(reverse("auth_view_router"))

    # GETting the auth_view_router redirects the user to the login URL.
    assert 302 == response.status_code
    assert f"{reverse('login')}?next={reverse('auth_view_router')}" == response.url
    assert mock_get_home_page_url.called is False


@pytest.mark.parametrize(
    "group_names,expected_redirect",
    [
        ([], "get_home_page_url"),
        (["Closed POD"], "get_closedpod_home_page_url"),
        (["PCW MSA"], "get_pcwmsa_home_page_url"),
        (["Big Cities"], "get_home_page_url"),
        (["Closed POD", "PCW MSA"], "get_closedpod_home_page_url"),
        (["Closed POD", "Big Cities"], "get_closedpod_home_page_url"),
        (["PCW MSA", "Big Cities"], "get_pcwmsa_home_page_url"),
        (["Closed POD", "PCW MSA", "Big Cities"], "get_closedpod_home_page_url"),
    ],
)
def test_authenticated_view_router_authenticated(
    db, client, mocker, group_names, expected_redirect
):
    """Authenticated users get redirected, based on their Group(s)."""
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.hip.views.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url
    # Mock the apps.common.utils.get_closedpod_home_page_url function, since it
    # is used to determine the Closed POD homepage URL.
    mock_get_closedpod_home_page_url = mocker.patch(
        "apps.hip.views.get_closedpod_home_page_url"
    )
    mock_closedpod_homepage_url = "/the_closedpod_home_page_url/"
    mock_get_closedpod_home_page_url.return_value = mock_closedpod_homepage_url
    # Mock the apps.common.utils.get_pcwmsa_home_page_url function, since it
    # is used to determine the PCW MSA homepage URL.
    mock_get_pcwmsa_home_page_url = mocker.patch(
        "apps.hip.views.get_pcwmsa_home_page_url"
    )
    mock_pcwmsa_homepage_url = "/the_pcwmsa_home_page_url/"
    mock_get_pcwmsa_home_page_url.return_value = mock_pcwmsa_homepage_url

    # Create a user, and put the user into a particular Group.
    user = UserFactory(email="test-user")
    Group.objects.all().delete()
    for group_name in group_names:
        group = GroupFactory(name=group_name)
        group.save()
        user.groups.add(group)
    # Log in the user.
    client.force_login(user)

    response = client.get(reverse("auth_view_router"))

    # GETting the login page redirects the user to the expected_redirect.
    assert 302 == response.status_code
    if expected_redirect == "get_home_page_url":
        assert mock_homepage_url == response.url
    elif expected_redirect == "get_closedpod_home_page_url":
        assert mock_closedpod_homepage_url == response.url
    elif expected_redirect == "get_pcwmsa_home_page_url":
        assert mock_pcwmsa_homepage_url == response.url

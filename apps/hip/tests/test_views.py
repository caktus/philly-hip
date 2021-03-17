from django.shortcuts import reverse

import pytest

from apps.users.tests.factories import UserFactory


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


def test_hip_login_view_get_unauthenticated(db, client):
    """An unauthenticated user GETting the login page sees the login page."""
    response = client.get(reverse("login"))
    assert 200 == response.status_code
    assert ["registration/login.html"] == response.template_name


def test_hip_login_view_get_authenticated(db, client, mocker):
    """An authenticated user GETting the login page is redirected to the homepage URL."""
    # Mock the apps.common.utils.get_home_page_url function, since the it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.hip.views.get_home_page_url")
    mock_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_url

    # Log in the user.
    user = UserFactory(email="test-user")
    client.force_login(user)

    response = client.get(reverse("login"))

    # GETting the login page redirects the user to the get_home_page_url().
    assert 302 == response.status_code
    assert mock_url == response.url

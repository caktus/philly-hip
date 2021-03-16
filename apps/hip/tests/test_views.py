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
    if post_data is not None:
        post_data["remember_me"] = remember_me
    response = client.post(reverse("login"), post_data)

    # The session is now set to expire when the browser is closed.
    assert client.session.get_expire_at_browser_close() is True

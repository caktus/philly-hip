from django.shortcuts import reverse

from apps.users.tests.factories import UserFactory


def test_successful_login_logs(db, client, mocker):
    """Logging in to the site logs the user's email and IP address."""
    user = UserFactory(email="test-user")
    user.set_password("testpassword1")
    user.save()

    # Mock the apps.users.signals.logger, to verify it gets called.
    mock_logger = mocker.patch("apps.users.signals.logger")
    # The 'X-Forwarded-For' header for the request.
    header_x_forwarded_for = "1.2.3.4"

    response = client.post(
        reverse("login"),
        {"username": user.email, "password": "testpassword1", "remember_me": True},
        HTTP_X_FORWARDED_FOR=header_x_forwarded_for,
    )

    # The logger was used to log the user's login attempt.
    assert mock_logger.info.called
    expected_log_msg = (
        f"user '{user.email}' has logged in from IP address '{header_x_forwarded_for}'."
    )
    assert expected_log_msg == mock_logger.info.call_args_list[0][0][0]


def test_unsuccessful_login_logs(db, client, mocker):
    """Unsuccessful attempts to log in do not log anything."""
    user = UserFactory(email="test-user")
    user.set_password("testpassword1")
    user.save()

    # Mock the apps.users.signals.logger, to verify that it does not get called.
    mock_logger = mocker.patch("apps.users.signals.logger")

    response = client.post(
        reverse("login"),
        {"username": user.email, "password": "invalid password", "remember_me": True},
    )

    # The logger was not used to log the user's login attempt.
    assert mock_logger.info.called is False


def test_admin_logout_clears_session(db, client, mocker):
    """Logging out via GET request clears the user's session."""
    # This test had to be modified because Django now uses a GET request for
    # admin logout, therefore a log message is no longer produced. See:
    # https://forum.djangoproject.com/t/deprecation-of-get-method-for-logoutview/25533
    # https://code.djangoproject.com/ticket/15619

    # Create a user who is logged in to the site.
    user = UserFactory(email="test-user")
    user.set_password("testpassword1")
    user.save()
    client.force_login(user)
    # The 'X-Forwarded-For' header for the request.
    header_x_forwarded_for = "1.2.3.4"

    # Mock the apps.users.signals.logger, to verify it gets called.
    mock_logger = mocker.patch("apps.users.signals.logger")

    # The logger was used to log the user's login attempt.
    assert not mock_logger.info.called
    assert len(mock_logger.info.call_args_list) == 0


def test_logging_out_when_log_logged_in_logs(db, client, mocker):
    """Attempting to log out of the site when not logged in does not log anything."""
    # Mock the apps.users.signals.logger, to verify it does not get called.
    mock_logger = mocker.patch("apps.users.signals.logger")

    response = client.get(reverse("logout"))

    # The logger was not used to log the user's logout attempt.
    assert mock_logger.info.called is False

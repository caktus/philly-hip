from http import HTTPStatus

from django.contrib.messages import get_messages
from django.urls import reverse

import pytest
from pytest_django.asserts import assertTemplateUsed

from ..forms import (
    CodeRedCodeBlueSubscriberForm,
    CommunityResponseSubscriberForm,
    DrugOverdoseSubscriberForm,
    InternalAlertsSubscriberForm,
    PublicHealthPreparednessSubscriberForm,
)


def test_get_internal_alerts_signup_page(db, client):
    """GETting the internal alerts signup page shows the form to the user."""
    response = client.get(reverse("internal_alerts_signup"))
    assert HTTPStatus.OK == response.status_code
    assertTemplateUsed("notifications/subscriber_signup.html")
    assert isinstance(response.context["form"], InternalAlertsSubscriberForm)


@pytest.mark.parametrize(
    "next_url,http_referrer_header,expected_success_url",
    [
        ("", "", "/the_emergency_communications_page/"),
        ("/next_url/", "", "/next_url/"),
        ("", "/http_referrer_header/", "/http_referrer_header/"),
        ("/next_url/", "/http_referrer_header/", "/next_url/"),
    ],
)
def test_internal_alerts_signup_valid_data(
    db,
    client,
    mocker,
    internal_alert_data,
    next_url,
    http_referrer_header,
    expected_success_url,
):
    """
    POSTting valid data redirects the user, and shows a success message.

    If the request has a "next" parameter, then the user should be sent to that URL.
    Otherwise, if the request has an HTTP_REFERER header, then the user should be
    redirected to it.
    Otherwise, the get_emergency_communications_page_url() utility function is
    used to determine where the user should be redirected to.
    """
    # Mock the get_emergency_communications_page() function, since it is sometimes
    # used to determine the redirect URL for a successful POST.
    mock_get_emergency_communications_page_url = mocker.patch(
        "apps.notifications.views.get_emergency_communications_page_url"
    )
    mock_url = "/the_emergency_communications_page/"
    mock_get_emergency_communications_page_url.return_value = mock_url

    url = reverse("internal_alerts_signup")
    if next_url:
        url += f"?next={next_url}"
    if http_referrer_header:
        response = client.post(
            url, internal_alert_data, HTTP_REFERER=http_referrer_header
        )
    else:
        response = client.post(url, internal_alert_data)

    assert HTTPStatus.FOUND == response.status_code
    assert expected_success_url == response.url
    messages = get_messages(response.wsgi_request)
    expected_message = (
        "You are now subscribed to alerts from the Philadelphia Department of "
        "Public Health Internal Employee Alert System"
    )
    assert expected_success_url == response.url
    assert [str(message) for message in messages] == [expected_message]
    # If the expected_success_url is neither the next_url nor the http_referrer_header,
    # then it must be from the mocked get_emergency_communications_page() function,
    # so verify that the get_emergency_communications_page() function was called.
    if expected_success_url not in [next_url, http_referrer_header]:
        assert 1 == mock_get_emergency_communications_page_url.call_count


def test_internal_alerts_signup_invalid_data(db, client, internal_alert_data):
    """POSTting invalid data shows errors to the user."""
    data = internal_alert_data.copy()
    data.pop("first_name")

    response = client.post(reverse("internal_alerts_signup"), data)

    assert HTTPStatus.OK == response.status_code
    assert "This field is required." in str(response.content)
    assert {"first_name": ["This field is required."]} == response.context[
        "form"
    ].errors


def test_get_community_response_notification_signup_page(db, client):
    """GETting the community response notification signup page shows the form to the user."""
    response = client.get(reverse("community_notifications_signup"))
    assert HTTPStatus.OK == response.status_code
    assertTemplateUsed("notifications/subscriber_signup.html")
    assert isinstance(response.context["form"], CommunityResponseSubscriberForm)


@pytest.mark.parametrize(
    "next_url,http_referrer_header,expected_success_url",
    [
        ("", "", "/the_emergency_communications_page/"),
        ("/next_url/", "", "/next_url/"),
        ("", "/http_referrer_header/", "/http_referrer_header/"),
        ("/next_url/", "/http_referrer_header/", "/next_url/"),
    ],
)
def test_community_response_notification_signup_valid_data(
    db,
    client,
    mocker,
    community_response_notification_data,
    next_url,
    http_referrer_header,
    expected_success_url,
):
    """
    POSTting valid data redirects the user, and shows a success message.

    If the request has a "next" parameter, then the user should be sent to that URL.
    Otherwise, if the request has an HTTP_REFERER header, then the user should be
    redirected to it.
    Otherwise, the get_emergency_communications_page_url() utility function is
    used to determine where the user should be redirected to.
    """
    # Mock the get_emergency_communications_page() function, since it is sometimes
    # used to determine the redirect URL for a successful POST.
    mock_get_emergency_communications_page_url = mocker.patch(
        "apps.notifications.views.get_emergency_communications_page_url"
    )
    mock_url = "/the_emergency_communications_page/"
    mock_get_emergency_communications_page_url.return_value = mock_url

    url = reverse("community_notifications_signup")
    if next_url:
        url += f"?next={next_url}"
    if http_referrer_header:
        response = client.post(
            url, community_response_notification_data, HTTP_REFERER=http_referrer_header
        )
    else:
        response = client.post(url, community_response_notification_data)

    assert HTTPStatus.FOUND == response.status_code
    assert expected_success_url == response.url
    messages = get_messages(response.wsgi_request)
    expected_message = (
        "You are now subscribed to notifications from the Philadelphia Department "
        "of Public Health for sharing with communities within Philadelphia."
    )
    assert [str(message) for message in messages] == [expected_message]
    # If the expected_success_url is neither the next_url nor the http_referrer_header,
    # then it must be from the mocked get_emergency_communications_page() function,
    # so verify that the get_emergency_communications_page() function was called.
    if expected_success_url not in [next_url, http_referrer_header]:
        assert 1 == mock_get_emergency_communications_page_url.call_count


def test_community_response_notification_signup_invalid_data(
    db, client, community_response_notification_data
):
    """POSTting invalid data shows errors to the user."""
    data = community_response_notification_data.copy()
    data.pop("email_address")

    response = client.post(reverse("community_notifications_signup"), data)

    assert HTTPStatus.OK == response.status_code
    assert {"email_address": ["This field is required."]} == response.context[
        "form"
    ].errors


def test_get_drug_overdose_notification_signup_page(db, client):
    """GETting the drug overdose signup page shows the form to the user."""
    response = client.get(reverse("drug_notifications_signup"))
    assert HTTPStatus.OK == response.status_code
    assertTemplateUsed("notifications/subscriber_signup.html")
    assert isinstance(response.context["form"], DrugOverdoseSubscriberForm)


@pytest.mark.parametrize(
    "next_url,http_referrer_header,expected_success_url",
    [
        ("", "", "/the_emergency_communications_page/"),
        ("/next_url/", "", "/next_url/"),
        ("", "/http_referrer_header/", "/http_referrer_header/"),
        ("/next_url/", "/http_referrer_header/", "/next_url/"),
    ],
)
def test_drug_overdose_notification_signup_valid_data(
    db,
    client,
    mocker,
    drug_overdose_notification_data,
    next_url,
    http_referrer_header,
    expected_success_url,
):
    """
    POSTting valid data redirects the user, and shows a success message.

    If the request has a "next" parameter, then the user should be sent to that URL.
    Otherwise, if the request has an HTTP_REFERER header, then the user should be
    redirected to it.
    Otherwise, the get_emergency_communications_page_url() utility function is
    used to determine where the user should be redirected to.
    """
    # Mock the get_emergency_communications_page() function, since it is sometimes
    # used to determine the redirect URL for a successful POST.
    mock_get_emergency_communications_page_url = mocker.patch(
        "apps.notifications.views.get_emergency_communications_page_url"
    )
    mock_url = "/the_emergency_communications_page/"
    mock_get_emergency_communications_page_url.return_value = mock_url

    url = reverse("drug_notifications_signup")
    if next_url:
        url += f"?next={next_url}"
    if http_referrer_header:
        response = client.post(
            url, drug_overdose_notification_data, HTTP_REFERER=http_referrer_header
        )
    else:
        response = client.post(url, drug_overdose_notification_data)

    assert HTTPStatus.FOUND == response.status_code
    assert expected_success_url == response.url
    messages = get_messages(response.wsgi_request)
    expected_message = (
        "You are now subscribed to notifications from the Philadelphia Department "
        "of Public Health related to drug overdoses."
    )
    assert [str(message) for message in messages] == [expected_message]
    # If the expected_success_url is neither the next_url nor the http_referrer_header,
    # then it must be from the mocked get_emergency_communications_page() function,
    # so verify that the get_emergency_communications_page() function was called.
    if expected_success_url not in [next_url, http_referrer_header]:
        assert 1 == mock_get_emergency_communications_page_url.call_count


def test_drug_overdose_notification_signup_invalid_data(
    db, client, drug_overdose_notification_data
):
    """POSTting invalid data shows errors to the user."""
    data = drug_overdose_notification_data.copy()
    data.pop("first_name")

    response = client.post(reverse("drug_notifications_signup"), data)

    assert HTTPStatus.OK == response.status_code
    assert {"first_name": ["This field is required."]} == response.context[
        "form"
    ].errors


def test_get_codeblue_codered_notifications_signup_page(db, client):
    """GETting the Code Blue/Code Red signup page shows the form to the user."""
    response = client.get(reverse("codeblue_codered_notifications_signup"))
    assert HTTPStatus.OK == response.status_code
    assertTemplateUsed("notifications/subscriber_signup.html")
    assert isinstance(response.context["form"], CodeRedCodeBlueSubscriberForm)


@pytest.mark.parametrize(
    "next_url,http_referrer_header,expected_success_url",
    [
        ("", "", "/the_emergency_communications_page/"),
        ("/next_url/", "", "/next_url/"),
        ("", "/http_referrer_header/", "/http_referrer_header/"),
        ("/next_url/", "/http_referrer_header/", "/next_url/"),
    ],
)
def test_codeblue_codered_notifications_signup_valid_data(
    db,
    client,
    mocker,
    codered_codeblue_notification_data,
    next_url,
    http_referrer_header,
    expected_success_url,
):
    """
    POSTting valid data redirects the user, and shows a success message.

    If the request has a "next" parameter, then the user should be sent to that URL.
    Otherwise, if the request has an HTTP_REFERER header, then the user should be
    redirected to it.
    Otherwise, the get_emergency_communications_page_url() utility function is
    used to determine where the user should be redirected to.
    """
    # Mock the get_emergency_communications_page() function, since it is sometimes
    # used to determine the redirect URL for a successful POST.
    mock_get_emergency_communications_page_url = mocker.patch(
        "apps.notifications.views.get_emergency_communications_page_url"
    )
    mock_url = "/the_emergency_communications_page/"
    mock_get_emergency_communications_page_url.return_value = mock_url

    url = reverse("codeblue_codered_notifications_signup")
    if next_url:
        url += f"?next={next_url}"
    if http_referrer_header:
        response = client.post(
            url, codered_codeblue_notification_data, HTTP_REFERER=http_referrer_header
        )
    else:
        response = client.post(url, codered_codeblue_notification_data)

    assert HTTPStatus.FOUND == response.status_code
    assert expected_success_url == response.url
    messages = get_messages(response.wsgi_request)
    expected_message = (
        "You are now subscribed to notifications from the Philadelphia Department "
        "of Public Health related to Code Red/Code Blue events."
    )
    assert [str(message) for message in messages] == [expected_message]
    # If the expected_success_url is neither the next_url nor the http_referrer_header,
    # then it must be from the mocked get_emergency_communications_page() function,
    # so verify that the get_emergency_communications_page() function was called.
    if expected_success_url not in [next_url, http_referrer_header]:
        assert 1 == mock_get_emergency_communications_page_url.call_count


def test_codeblue_codered_notifications_signup_invalid_data(db, client):
    """POSTting invalid data shows errors to the user."""
    data = {}
    response = client.post(reverse("codeblue_codered_notifications_signup"), data)
    assert HTTPStatus.OK == response.status_code
    expected_error = {"__all__": ["Please fill in at least 1 field."]}
    assert expected_error == response.context["form"].errors


def test_get_public_health_preparedness_signup_page(db, client):
    """GETting the public health preparedness signup page shows the form to the user."""
    response = client.get(reverse("public_health_preparedness_signup"))
    assert HTTPStatus.OK == response.status_code
    assertTemplateUsed("notifications/subscriber_signup.html")
    assert isinstance(response.context["form"], PublicHealthPreparednessSubscriberForm)


@pytest.mark.parametrize(
    "next_url,http_referrer_header,expected_success_url",
    [
        ("", "", "/the_emergency_communications_page/"),
        ("/next_url/", "", "/next_url/"),
        ("", "/http_referrer_header/", "/http_referrer_header/"),
        ("/next_url/", "/http_referrer_header/", "/next_url/"),
    ],
)
def test_public_health_preparedness_signup_valid_data(
    db,
    client,
    mocker,
    php_notification_data,
    next_url,
    http_referrer_header,
    expected_success_url,
):
    """
    POSTting valid data redirects the user, and shows a success message.

    If the request has a "next" parameter, then the user should be sent to that URL.
    Otherwise, if the request has an HTTP_REFERER header, then the user should be
    redirected to it.
    Otherwise, the get_emergency_communications_page_url() utility function is
    used to determine where the user should be redirected to.
    """
    # Mock the get_emergency_communications_page() function, since it is sometimes
    # used to determine the redirect URL for a successful POST.
    mock_get_emergency_communications_page_url = mocker.patch(
        "apps.notifications.views.get_emergency_communications_page_url"
    )
    mock_url = "/the_emergency_communications_page/"
    mock_get_emergency_communications_page_url.return_value = mock_url

    url = reverse("public_health_preparedness_signup")
    if next_url:
        url += f"?next={next_url}"
    if http_referrer_header:
        response = client.post(
            url, php_notification_data, HTTP_REFERER=http_referrer_header
        )
    else:
        response = client.post(url, php_notification_data)

    assert HTTPStatus.FOUND == response.status_code
    assert expected_success_url == response.url
    messages = get_messages(response.wsgi_request)
    expected_message = (
        "You are now subscribed to notifications from the Philadelphia Department "
        "of Public Health related to public health preparedness."
    )
    assert [str(message) for message in messages] == [expected_message]
    # If the expected_success_url is neither the next_url nor the http_referrer_header,
    # then it must be from the mocked get_emergency_communications_page() function,
    # so verify that the get_emergency_communications_page() function was called.
    if expected_success_url not in [next_url, http_referrer_header]:
        assert 1 == mock_get_emergency_communications_page_url.call_count
    else:
        assert 0 == mock_get_emergency_communications_page_url.call_count


def test_public_health_preparedness_signup_invalid_data(
    db, client, php_notification_data
):
    """POSTting invalid data shows errors to the user."""
    data = php_notification_data.copy()
    data.pop("first_name")

    response = client.post(reverse("public_health_preparedness_signup"), data)

    assert HTTPStatus.OK == response.status_code
    assert {"first_name": ["This field is required."]} == response.context[
        "form"
    ].errors

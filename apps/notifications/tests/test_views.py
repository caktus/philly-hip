from http import HTTPStatus

from django.contrib.messages import get_messages
from django.urls import reverse

from pytest_django.asserts import assertTemplateUsed

from ..forms import (
    CodeBlueCodeRedSubscriberForm,
    CommunityResponseSubscriberForm,
    InternalAlertsSubscriberForm,
    OpioidOverdoseSubscriberForm,
    PublicHealthPreparednessSubscriberForm,
)


def test_get_internal_alerts_signup_page(db, client):
    """GETting the internal alerts signup page shows the form to the user."""
    response = client.get(reverse("internal_alerts_signup"))
    assert HTTPStatus.OK == response.status_code
    assertTemplateUsed("notifications/subscriber_signup.html")
    assert isinstance(response.context["form"], InternalAlertsSubscriberForm)


def test_internal_alerts_signup_valid_data_no_previous_referrer(
    db, client, mocker, internal_alert_data
):
    """
    POSTting valid data redirects the user, and shows a success message.

    If the request has no HTTP_REFERER, then the get_emergency_communications_page_url()
    utility function is used to determine where the user should be redirected upon
    POSTing valid data.
    """
    # The request in this test has no HTTP_REFERER header, so we mock the
    # get_emergency_communications_page() function, since it is used to determine
    # the URL for a successful POST.
    mock_get_emergency_communications_page_url = mocker.patch(
        "apps.notifications.views.get_emergency_communications_page_url"
    )
    mock_url = "/the_emergency_communications_page/"
    mock_get_emergency_communications_page_url.return_value = mock_url

    response = client.post(reverse("internal_alerts_signup"), internal_alert_data)

    assert HTTPStatus.FOUND == response.status_code
    messages = get_messages(response.wsgi_request)
    expected_message = (
        "You are now subscribed to alerts from the Philadelphia Department of "
        "Public Health Internal Employee Alert System"
    )
    assert mock_url == response.url
    assert [str(message) for message in messages] == [expected_message]


def test_internal_alerts_signup_valid_data_with_previous_referrer(
    db, client, internal_alert_data
):
    """
    POSTting valid data redirects the user, and shows a success message.

    If the request has an HTTP_REFERER, then the user is redirected to it upon
    POSTing valid data.
    """
    # The request in this test has an HTTP_REFERER header.
    http_referrer_header = "/the_last_page_url/"

    response = client.post(
        reverse("internal_alerts_signup"),
        internal_alert_data,
        HTTP_REFERER=http_referrer_header,
    )

    assert HTTPStatus.FOUND == response.status_code
    # Since the request in this test has an HTTP_REFERER header, that header should
    # be used as the URL the user is redirected to.
    assert http_referrer_header == response.url
    messages = get_messages(response.wsgi_request)
    expected_message = (
        "You are now subscribed to alerts from the Philadelphia Department of "
        "Public Health Internal Employee Alert System"
    )
    assert [str(message) for message in messages] == [expected_message]


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


def test_community_response_notification_signup_valid_data(db, client):
    """POSTting valid data redirects the user, and shows a success message."""
    response = client.post(reverse("community_notifications_signup"), {})
    messages = get_messages(response.wsgi_request)
    expected_message = (
        "You are now subscribed to notifications from the Philadelphia Department "
        "of Public Health for sharing with communities within Philadelphia."
    )
    assert "/" == response.url
    assert HTTPStatus.FOUND == response.status_code
    assert [str(message) for message in messages] == [expected_message]


# TODO: implement in DIS-1700
# def test_community_response_notification_signup_invalid_data(db, client):
#     """POSTting invalid data shows errors to the user."""
#     data = {}
#     expected_errors = []
#     response = client.post(reverse("community_notifications_signup"), data)
#     assert HTTPStatus.OK == response.status_code
#     for error in expected_errors:
#         assert error in str(response.content)


def test_get_opioid_overdose_notification_signup_page(db, client):
    """GETting the opioid overdose signup page shows the form to the user."""
    response = client.get(reverse("opioid_notifications_signup"))
    assert HTTPStatus.OK == response.status_code
    assertTemplateUsed("notifications/subscriber_signup.html")
    assert isinstance(response.context["form"], OpioidOverdoseSubscriberForm)


def test_opioid_overdose_notification_signup_valid_data(db, client):
    """POSTting valid data redirects the user, and shows a success message."""
    response = client.post(reverse("opioid_notifications_signup"), {})
    messages = get_messages(response.wsgi_request)
    expected_message = (
        "You are now subscribed to notifications from the Philadelphia Department "
        "of Public Health related to opioid overdoses."
    )
    assert "/" == response.url
    assert HTTPStatus.FOUND == response.status_code
    assert [str(message) for message in messages] == [expected_message]


# TODO: implement in DIS-1700
# def test_opioid_overdose_notification_signup_invalid_data(db, client):
#     """POSTting invalid data shows errors to the user."""
#     data = {}
#     expected_errors = []
#     response = client.post(reverse("opioid_notifications_signup"), data)
#     assert HTTPStatus.OK == response.status_code
#     for error in expected_errors:
#         assert error in str(response.content)


def test_get_codeblue_codered_notifications_signup_page(db, client):
    """GETting the Code Blue/Code Red signup page shows the form to the user."""
    response = client.get(reverse("codeblue_codered_notifications_signup"))
    assert HTTPStatus.OK == response.status_code
    assertTemplateUsed("notifications/subscriber_signup.html")
    assert isinstance(response.context["form"], CodeBlueCodeRedSubscriberForm)


def test_codeblue_codered_notifications_signup_valid_data(db, client):
    """POSTting valid data redirects the user, and shows a success message."""
    response = client.post(reverse("codeblue_codered_notifications_signup"), {})
    messages = get_messages(response.wsgi_request)
    expected_message = (
        "You are now subscribed to notifications from the Philadelphia Department "
        "of Public Health related to Code Red/Code Blue events."
    )
    assert "/" == response.url
    assert HTTPStatus.FOUND == response.status_code
    assert [str(message) for message in messages] == [expected_message]


# TODO: implement in DIS-1700
# def test_codeblue_codered_notifications_signup_invalid_data(db, client):
#     """POSTting invalid data shows errors to the user."""
#     data = {}
#     expected_errors = []
#     response = client.post(reverse("codeblue_codered_notifications_signup"), data)
#     assert HTTPStatus.OK == response.status_code
#     for error in expected_errors:
#         assert error in str(response.content)


def test_get_public_health_preparedness_signup_page(db, client):
    """GETting the public health preparedness signup page shows the form to the user."""
    response = client.get(reverse("public_health_preparedness_signup"))
    assert HTTPStatus.OK == response.status_code
    assertTemplateUsed("notifications/subscriber_signup.html")
    assert isinstance(response.context["form"], PublicHealthPreparednessSubscriberForm)


def test_public_health_preparedness_signup_valid_data(db, client):
    """POSTting valid data redirects the user, and shows a success message."""
    response = client.post(reverse("public_health_preparedness_signup"), {})
    messages = get_messages(response.wsgi_request)
    expected_message = (
        "You are now subscribed to notifications from the Philadelphia Department "
        "of Public Health related to public health preparedness."
    )
    assert "/" == response.url
    assert HTTPStatus.FOUND == response.status_code
    assert [str(message) for message in messages] == [expected_message]


# TODO: implement in DIS-1700
# def test_public_health_preparedness_signup_invalid_data(db, client):
#     """POSTting invalid data shows errors to the user."""
#     data = {}
#     expected_errors = []
#     response = client.post(reverse("public_health_preparedness_signup"), data)
#     assert HTTPStatus.OK == response.status_code
#     for error in expected_errors:
#         assert error in str(response.content)

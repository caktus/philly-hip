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


def test_internal_alerts_signup_valid_data(db, client):
    """POSTting valid data redirects the user, and shows a success message."""
    response = client.post(reverse("internal_alerts_signup"), {})
    messages = get_messages(response.wsgi_request)
    expected_message = (
        "You are now subscribed to alerts from the Philadelphia Department of "
        "Public Health Internal Employee Alert System"
    )
    assert "/" == response.url
    assert HTTPStatus.FOUND == response.status_code
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

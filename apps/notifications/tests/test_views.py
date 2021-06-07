from http import HTTPStatus

from django.contrib.messages import get_messages
from django.urls import reverse

from pytest_django.asserts import assertTemplateUsed

from ..forms import InternalAlertsSubscriberForm


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


# TODO: implement in DIS-1700
# def test_internal_alerts_signup_invalid_data(db, client):
#     """POSTting invalid data shows errors to the user."""
#     data = {}
#     expected_errors = []
#     response = client.post(reverse("internal_alerts_signup"), data)
#     assert HTTPStatus.OK == response.status_code
#     for error in expected_errors:
#         assert error in str(response.content)

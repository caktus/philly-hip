from http import HTTPStatus

from django.contrib.messages import get_messages
from django.urls import reverse

import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.fixture
def subscribe_data():
    return dict(
        personal_first_name="SpongeBob",
        personal_last_name="SquarePants",
        personal_medical_expertise="Sutures",
        personal_professional_license="1294dk",
        agency_name="The Crabby Patty",
        agency_type="PDPH",
        agency_zip_code="12340",
        agency_position="Manager",
        network_email="crabbypatty@gmail.com",
        network_fax="(201) 555-0123",
    )


@pytest.fixture
def url():
    return reverse("health_alert_subscriber")


def test_get_subscribe_page(db, client, url):
    res = client.get(url)
    assert HTTPStatus.OK == res.status_code
    assertTemplateUsed("health_alerts/health_alert_subscriber.html")
    assert "form" in res.context


def test_success_msg_queqed_and_user_redirects(db, client, url, subscribe_data):
    res = client.post(url, subscribe_data)
    messages = get_messages(res.wsgi_request)
    success_msg = (
        "You are now subscribed to receiving Health Alerts "
        "from the Philadelphia Department of Public Health."
    )
    assert res.url == "/health-alerts/"
    assert HTTPStatus.FOUND == res.status_code
    assert str(list(messages)[0]) == success_msg


def test_form_errors_raised(db, client, url, subscribe_data):
    data = subscribe_data
    data["network_fax"] = "failure"
    res = client.post(url, data)
    error_msg = (
        "Enter a valid phone number (e.g. (201) 555-0123) or a number "
        "with an international call prefix."
    )
    assert HTTPStatus.OK == res.status_code
    assert error_msg in str(res.content)


def test_form_errors_raised_multiple(db, client, url, subscribe_data):
    errors = []
    # This field is required error
    del subscribe_data["personal_first_name"]
    field_required_error = "This field is required."
    errors.append(field_required_error)

    # network fax error
    subscribe_data["network_fax"] = "23903203"
    network_fax_error = (
        "Enter a valid phone number (e.g. (201) 555-0123) or a number "
        "with an international call prefix."
    )
    errors.append(network_fax_error)
    # zip_code error
    subscribe_data["agency_zip_code"] = "23903203"
    zip_code_error = "Either provide a 5 or 9 digit zipcode Ex: 12345 or 12345-1234"
    errors.append(zip_code_error)
    res = client.post(url, subscribe_data)
    for e in errors:
        assert e in str(res.content)

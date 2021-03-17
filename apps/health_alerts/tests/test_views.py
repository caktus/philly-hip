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


def test_get_subscribe_page(db, settings, client, url):
    settings.STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
    res = client.get(url)
    assert HTTPStatus.OK == res.status_code
    assertTemplateUsed("health_alerts/health_alert_subscriber.html")
    assert "form" in res.context


def test_success_msg_queqed_and_user_redirects(
    db, settings, client, url, subscribe_data
):
    settings.STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
    res = client.post(url, subscribe_data)
    messages = get_messages(res.wsgi_request)
    success_msg = (
        "You are now subscribed to receiving Health Alerts "
        "from the Philadelphia Department of Public Health."
    )
    assert res.url == "/health-alerts/"
    assert HTTPStatus.FOUND == res.status_code
    assert str(list(messages)[0]) == success_msg


def test_form_errors_raised(db, settings, client, url, subscribe_data):
    settings.STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
    data = subscribe_data
    data["network_fax"] = "failure"
    res = client.post(url, data)
    error_msg = (
        "Enter a valid phone number (e.g. (201) 555-0123) or a number "
        "with an international call prefix."
    )
    assert HTTPStatus.OK == res.status_code
    assert error_msg in str(res.content)

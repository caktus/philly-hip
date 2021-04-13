from http import HTTPStatus

from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.urls import reverse

import pytest
from pytest_django.asserts import assertTemplateUsed

from apps.users.tests.factories import UserFactory

from .factories import ClosedPODContactInformationFactory


@pytest.fixture
def contact_information_data():
    return {
        "facility_name": "New Facility",
        "facility_id": "A123",
        "phone_number": "(215) 555-4444",
        "primary_contact_name": "Me",
        "primary_contact_work_email": "me@phila.gov",
        "primary_contact_personal_email": "me@myemail.com",
        "primary_contact_cell_phone": "(267) 345-6789",
        "primary_contact_cell_phone_provider": "AT&T",
        "secondary_contact_name": "Someone Else",
        "secondary_contact_work_email": "someoneelse@phila.gov",
        "secondary_contact_personal_email": "someoneelse@example.com",
        "secondary_contact_cell_phone": "610 333-4444",
        "secondary_contact_cell_phone_provider": "Verizon",
    }


def test_get_closedpod_contact_information_unauthenticated(db, client):
    """An unauthenticated user is redirected to log in."""
    url = reverse("closedpod_contact_information")
    response = client.get(url)
    assert HTTPStatus.FOUND == response.status_code
    assert f"{reverse('login')}?next={url}" == response.url


def test_get_closedpod_contact_information_authenticated_not_in_any_group(db, client):
    """An authenticated user who is not in any Groups is redirected to log in."""
    url = reverse("closedpod_contact_information")
    user = UserFactory()
    client.force_login(user)
    assert not user.groups.exists()

    response = client.get(url)

    assert HTTPStatus.FOUND == response.status_code
    assert f"{reverse('login')}?next={url}" == response.url


def test_get_closedpod_contact_information_authenticated_in_other_group(db, client):
    """An authenticated user who is not in the "Closed POD" Group is redirected to log in."""
    url = reverse("closedpod_contact_information")
    user = UserFactory()
    # The user is in a Group, but not the "Closed POD" Group.
    user.groups.add(Group.objects.get(name="PCW MSA"))
    client.force_login(user)

    response = client.get(url)

    assert HTTPStatus.FOUND == response.status_code
    assert f"{reverse('login')}?next={url}" == response.url


def test_get_closedpod_contact_information_authenticated_in_closedpod_group_no_info(
    db, client
):
    """
    GET closedpod_contact_information view for an authenticated user in the "Closed POD" Group.

    An authenticated user who is in the "Closed POD" Group can see the page.
    However, if the user has no ClosedPODContactInformation, then the data is empty.
    """
    url = reverse("closedpod_contact_information")
    user = UserFactory()
    user.groups.add(Group.objects.get(name="Closed POD"))
    client.force_login(user)

    response = client.get(url)

    assert HTTPStatus.OK == response.status_code
    assertTemplateUsed("auth_content/closedpod_contact_information.html")
    assert response.context["contact_info"].id is None
    assert "" == response.context["contact_info"].facility_name


def test_get_closedpod_contact_information_authenticated_in_closedpod_group_with_info(
    db, client
):
    """
    GET closedpod_contact_information view for an authenticated user in the "Closed POD" Group.

    An authenticated user who is in the "Closed POD" Group can see the page.
    If the user has a ClosedPODContactInformation, then that data is in the context.
    """
    url = reverse("closedpod_contact_information")
    user = UserFactory()
    ClosedPODContactInformationFactory(user=user)
    user.groups.add(Group.objects.get(name="Closed POD"))
    client.force_login(user)

    response = client.get(url)

    assert HTTPStatus.OK == response.status_code
    assertTemplateUsed("auth_content/closedpod_contact_information.html")
    assert user.closedpodcontactinformation.id == response.context["contact_info"].id
    assert (
        user.closedpodcontactinformation.facility_name
        == response.context["contact_info"].facility_name
    )


@pytest.mark.parametrize("method_name", ["POST", "PATCH", "PUT", "DELETE"])
def test_closedpod_contact_information_unsupported_methods(db, client, method_name):
    """The closedpod_contact_information view supports only the GET method."""
    url = reverse("closedpod_contact_information")
    user = UserFactory()
    user.groups.add(Group.objects.get(name="Closed POD"))
    client.force_login(user)

    method = getattr(client, method_name.lower())
    response = method(url)

    assert HTTPStatus.METHOD_NOT_ALLOWED == response.status_code


@pytest.mark.parametrize("method_name", ["GET", "POST"])
def test_closedpod_contact_information_edit_unauthenticated(db, client, method_name):
    """An unauthenticated user is redirected to log in."""
    url = reverse("closedpod_contact_information_edit")
    method = getattr(client, method_name.lower())
    response = method(url)
    assert HTTPStatus.FOUND == response.status_code
    assert f"{reverse('login')}?next={url}" == response.url


@pytest.mark.parametrize("method_name", ["GET", "POST"])
def test_closedpod_contact_information_edit_authenticated_not_in_any_group(
    db, client, method_name
):
    """An authenticated user who is not in any Groups is redirected to log in."""
    url = reverse("closedpod_contact_information_edit")
    user = UserFactory()
    client.force_login(user)
    assert not user.groups.exists()

    method = getattr(client, method_name.lower())
    response = method(url)

    assert HTTPStatus.FOUND == response.status_code
    assert f"{reverse('login')}?next={url}" == response.url


@pytest.mark.parametrize("method_name", ["GET", "POST"])
def test_closedpod_contact_information_edit_authenticated_in_other_group(
    db, client, method_name
):
    """An authenticated user who is not in the "Closed POD" Group is redirected to log in."""
    url = reverse("closedpod_contact_information_edit")
    user = UserFactory()
    # The user is in a Group, but not the "Closed POD" Group.
    user.groups.add(Group.objects.get(name="PCW MSA"))
    client.force_login(user)

    method = getattr(client, method_name.lower())
    response = method(url)

    assert HTTPStatus.FOUND == response.status_code
    assert f"{reverse('login')}?next={url}" == response.url


def test_get_closedpod_contact_information_edit_authenticated_in_closedpod_group_no_info(
    db, client
):
    """
    GET closedpod_contact_information_edit view for an authenticated user in the "Closed POD" Group.

    An authenticated user who is in the "Closed POD" Group can see the page.
    If the user has no ClosedPODContactInformation, then the form has empty data.
    """
    url = reverse("closedpod_contact_information_edit")
    user = UserFactory()
    user.groups.add(Group.objects.get(name="Closed POD"))
    client.force_login(user)

    response = client.get(url)

    assert HTTPStatus.OK == response.status_code
    assertTemplateUsed("auth_content/closedpod_contact_information_edit.html")
    assert {} == response.context["form"].data


def test_post_closedpod_contact_information_edit_authenticated_in_closedpod_group_no_info_errors(
    db, client, contact_information_data
):
    """
    POST to closedpod_contact_information_edit view for an authenticated user in the "Closed POD" Group.

    An authenticated user who is in the "Closed POD" Group can POST to the view.
    POSTing empty data returns errors, and does not create a ClosedPODContactInformation
    object for the user.
    """
    url = reverse("closedpod_contact_information_edit")
    user = UserFactory()
    user.groups.add(Group.objects.get(name="Closed POD"))
    client.force_login(user)

    response = client.post(url, {})

    # Since the POST data is empty, the user sees errors on the page.
    # No ClosedPODContactInformation object is created for the request.user.
    assert HTTPStatus.OK == response.status_code
    assert response.context["form"].is_valid() is False
    expected_errors = {}
    for field_name in contact_information_data:
        expected_errors[field_name] = ["This field is required."]
    assert expected_errors == response.context["form"].errors
    user.refresh_from_db()
    assert not hasattr(user, "closedpodcontactinformation")
    # There is no success message for the user.
    messages = [str(message) for message in get_messages(response.wsgi_request)]
    assert [] == messages


def test_post_closedpod_contact_information_edit_authenticated_in_closedpod_group_create(
    db, client, contact_information_data
):
    """
    POST to closedpod_contact_information_edit view for an authenticated user in the "Closed POD" Group.

    An authenticated user who is in the "Closed POD" Group can POST to the view.
    If the user does not have a ClosedPODContactInformation, then POSTing to
    this view will create a new ClosedPODContactInformation for the user.
    """
    url = reverse("closedpod_contact_information_edit")
    user = UserFactory()
    user.groups.add(Group.objects.get(name="Closed POD"))
    client.force_login(user)

    response = client.post(url, contact_information_data)

    # POSTing valid data creates a ClosedPODContactInformation object for the
    # request.user, and redirects to the "closedpod_contact_information" view.
    assert HTTPStatus.FOUND == response.status_code
    assert reverse("closedpod_contact_information") == response.url
    messages = [str(message) for message in get_messages(response.wsgi_request)]
    assert ["Contact information has been updated"] == messages
    user.refresh_from_db()
    assert user.closedpodcontactinformation.id is not None


def test_get_closedpod_contact_information_edit_authenticated_in_closedpod_group_with_obj(
    db, client
):
    """
    GET closedpod_contact_information view for an authenticated user in the "Closed POD" Group.

    An authenticated user who is in the "Closed POD" Group can see the page.
    If the user has a ClosedPODContactInformation, then that data is in the form
    in the context.
    """
    url = reverse("closedpod_contact_information_edit")
    user = UserFactory()
    ClosedPODContactInformationFactory(user=user)
    user.groups.add(Group.objects.get(name="Closed POD"))
    client.force_login(user)

    response = client.get(url)

    assert HTTPStatus.OK == response.status_code
    assertTemplateUsed("auth_content/closedpod_contact_information_edit.html")
    # The user can see the data for their ClosedPODContactInformation on the page.
    assert (
        user.closedpodcontactinformation.facility_name
        == response.context["form"].initial["facility_name"]
    )


def test_post_closedpod_contact_information_edit_authenticated_in_closedpod_group_update(
    db, client, contact_information_data
):
    """
    POST to closedpod_contact_information view for an authenticated user in the "Closed POD" Group.

    An authenticated user who is in the "Closed POD" Group can POST to the page.
    If the user has a ClosedPODContactInformation, then that data may be updated.
    """
    url = reverse("closedpod_contact_information_edit")
    user = UserFactory()
    ClosedPODContactInformationFactory(user=user)
    user.groups.add(Group.objects.get(name="Closed POD"))
    client.force_login(user)

    response = client.post(url, contact_information_data)

    # POSTing valid data updates the ClosedPODContactInformation object for the
    # request.user, and redirects to the "closedpod_contact_information" view.
    assert HTTPStatus.FOUND == response.status_code
    assert reverse("closedpod_contact_information") == response.url
    messages = [str(message) for message in get_messages(response.wsgi_request)]
    assert ["Contact information has been updated"] == messages
    user.refresh_from_db()
    assert (
        user.closedpodcontactinformation.facility_name
        == contact_information_data["facility_name"]
    )


def test_post_closedpod_contact_information_edit_authenticated_in_closedpod_group_update_user(
    db, client, contact_information_data
):
    """
    POST to closedpod_contact_information view for an authenticated user in the "Closed POD" Group.

    An authenticated user who is in the "Closed POD" Group can POST to the page.
    However, a user may not edit the "user".
    """
    url = reverse("closedpod_contact_information_edit")
    user = UserFactory()
    ClosedPODContactInformationFactory(user=user)
    user.groups.add(Group.objects.get(name="Closed POD"))
    client.force_login(user)

    # Try to update the user for this ClosedPODContactInformation.
    other_user = UserFactory()
    data_with_other_user = contact_information_data
    data_with_other_user["user"] = other_user.id
    response = client.post(url, contact_information_data)

    # POSTing valid data does not update the  the ClosedPODContactInformation object for the
    # request.user, and redirects to the "closedpod_contact_information" view.
    assert HTTPStatus.FOUND == response.status_code
    assert reverse("closedpod_contact_information") == response.url
    user.refresh_from_db()
    assert user.closedpodcontactinformation.user == user


@pytest.mark.parametrize("method_name", ["PATCH", "PUT", "DELETE"])
def test_closedpod_contact_information_edit_unsupported_methods(
    db, client, method_name
):
    """The closedpod_contact_information_edit view supports only GET and POST methods."""
    url = reverse("closedpod_contact_information_edit")
    user = UserFactory()
    user.groups.add(Group.objects.get(name="Closed POD"))
    client.force_login(user)

    method = getattr(client, method_name.lower())
    response = method(url)

    assert HTTPStatus.METHOD_NOT_ALLOWED == response.status_code

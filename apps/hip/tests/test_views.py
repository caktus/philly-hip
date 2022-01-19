import os

from django.contrib.auth.models import Group
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.shortcuts import reverse

import pytest
from wagtail.core.models import Collection
from wagtail.documents import get_document_model

from apps.hip.tests.factories import DocumentFactory
from apps.users.tests.factories import GroupFactory, UserFactory

from ..forms import HIPAuthenticationForm


TESTDATA_DIR = os.path.join(os.path.dirname(__file__), "testdata")


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


def test_hip_login_view_post_no_next_parameter(db, client):
    """Logging in without a 'next' parameter means user is redirected to auth_view_router."""
    user = UserFactory(email="test-user")
    user.set_password("testpassword1")
    user.save()

    response = client.post(
        reverse("login"),
        {"username": user.email, "password": "testpassword1", "remember_me": True},
    )

    # The user is redirected to auth_view_router
    assert 302 == response.status_code
    assert reverse("auth_view_router") == response.url


def test_hip_login_view_post_with_next_parameter(db, client):
    """Logging in with a 'next' parameter means user is redirected to that parameter."""
    user = UserFactory(email="test-user")
    user.set_password("testpassword1")
    user.save()

    response = client.post(
        f"{reverse('login')}?next=next_page",
        {"username": user.email, "password": "testpassword1", "remember_me": True},
    )

    # The user is redirected to auth_view_router
    assert 302 == response.status_code
    assert "next_page" == response.url


def test_hip_login_view_get_unauthenticated(db, client):
    """An unauthenticated user GETting the login page sees the login page."""
    response = client.get(reverse("login"))
    assert 200 == response.status_code
    assert ["registration/login.html"] == response.template_name
    # The form used is the HIPAuthenticationForm.
    assert isinstance(response.context_data["form"], HIPAuthenticationForm) is True


def test_hip_login_view_get_authenticated(db, client):
    """An authenticated user GETting the login page is redirected to the auth_view_router."""
    # Log in the user.
    user = UserFactory(email="test-user")
    client.force_login(user)

    response = client.get(reverse("login"))

    # GETting the login page redirects the user to the auth_view_router view.
    assert 302 == response.status_code
    assert reverse("auth_view_router") == response.url


def test_authenticated_view_router_not_authenticated(db, client, mocker):
    """Unauthenticated users do not have access to the authenticated_view_router."""
    # Mock the apps.common.utils.get_home_page_url function, to verify it does
    # not get called.
    mock_get_home_page_url = mocker.patch("apps.hip.views.get_home_page_url")

    # A user is not logged in.
    client.logout()

    response = client.get(reverse("auth_view_router"))

    # GETting the auth_view_router redirects the user to the login URL.
    assert 302 == response.status_code
    assert f"{reverse('login')}?next={reverse('auth_view_router')}" == response.url
    assert mock_get_home_page_url.called is False


@pytest.mark.parametrize(
    "group_names,expected_redirect",
    [
        ([], "get_home_page_url"),
        (["Closed POD"], "get_closedpod_home_page_url"),
        (["PCW MSA"], "get_pcwmsa_home_page_url"),
        (["Big Cities"], "get_bigcities_home_page_url"),
        (["Closed POD", "PCW MSA"], "get_closedpod_home_page_url"),
        (["Closed POD", "Big Cities"], "get_closedpod_home_page_url"),
        (["PCW MSA", "Big Cities"], "get_pcwmsa_home_page_url"),
        (["Closed POD", "PCW MSA", "Big Cities"], "get_closedpod_home_page_url"),
    ],
)
def test_authenticated_view_router_authenticated(
    db, client, mocker, group_names, expected_redirect
):
    """Authenticated users get redirected, based on their Group(s)."""
    # Mock the apps.common.utils.get_home_page_url function, since it is used
    # to determine the homepage URL.
    mock_get_home_page_url = mocker.patch("apps.hip.views.get_home_page_url")
    mock_homepage_url = "/the_home_page_url/"
    mock_get_home_page_url.return_value = mock_homepage_url
    # Mock the apps.common.utils.get_closedpod_home_page_url function, since it
    # is used to determine the Closed POD homepage URL.
    mock_get_closedpod_home_page_url = mocker.patch(
        "apps.hip.views.get_closedpod_home_page_url"
    )
    mock_closedpod_homepage_url = "/the_closedpod_home_page_url/"
    mock_get_closedpod_home_page_url.return_value = mock_closedpod_homepage_url
    # Mock the apps.common.utils.get_pcwmsa_home_page_url function, since it
    # is used to determine the PCW MSA homepage URL.
    mock_get_pcwmsa_home_page_url = mocker.patch(
        "apps.hip.views.get_pcwmsa_home_page_url"
    )
    mock_pcwmsa_homepage_url = "/the_pcwmsa_home_page_url/"
    mock_get_pcwmsa_home_page_url.return_value = mock_pcwmsa_homepage_url
    # Mock the apps.common.utils.get_bigcities_home_page_url function, since it
    # is used to determine the Big Cities homepage URL.
    mock_get_bigcities_home_page_url = mocker.patch(
        "apps.hip.views.get_bigcities_home_page_url"
    )
    mock_bigcities_homepage_url = "/the_bigcities_home_page_url/"
    mock_get_bigcities_home_page_url.return_value = mock_bigcities_homepage_url

    # Create a user, and put the user into a particular Group.
    user = UserFactory(email="test-user")
    Group.objects.all().delete()
    for group_name in group_names:
        group = GroupFactory(name=group_name)
        group.save()
        user.groups.add(group)
    # Log in the user.
    client.force_login(user)

    response = client.get(reverse("auth_view_router"))

    # GETting the login page redirects the user to the expected_redirect.
    assert 302 == response.status_code
    if expected_redirect == "get_home_page_url":
        assert mock_homepage_url == response.url
    elif expected_redirect == "get_closedpod_home_page_url":
        assert mock_closedpod_homepage_url == response.url
    elif expected_redirect == "get_pcwmsa_home_page_url":
        assert mock_pcwmsa_homepage_url == response.url
    elif expected_redirect == "get_bigcities_home_page_url":
        assert mock_bigcities_homepage_url == response.url


def test_upload_document_get(db, client):
    """GETting the view to upload a document works."""
    # Log in the user.
    user = UserFactory(email="test-user")
    user.is_superuser = True
    user.save()
    client.force_login(user)

    response = client.get(reverse("wagtaildocs:add_multiple"))

    assert 200 == response.status_code


def test_upload_document_permission(db, client):
    """Regular users may not use the 'add_multiple' view."""
    # Log in the user.
    user = UserFactory(email="test-user")
    user.is_superuser = False
    user.is_staff = False
    user.save()
    client.force_login(user)

    response_get = client.get(reverse("wagtaildocs:add_multiple"))
    assert 403 == response_get.status_code
    response_post = client.post(reverse("wagtaildocs:add_multiple"))
    assert 403 == response_post.status_code


def test_upload_document_post(db, client):
    """
    Test uploading a Document in Wagtail.

    Since we have a custom HIPDocumentAddView, test that this view still works.
    """
    # Log in the user.
    user = UserFactory(email="test-user")
    user.is_superuser = True
    user.save()
    client.force_login(user)

    pdf_file_path = os.path.join(TESTDATA_DIR, "test.pdf")

    with open(pdf_file_path, "rb") as pdf_file:
        url = reverse("wagtaildocs:add_multiple")
        uploaded_file = TemporaryUploadedFile(
            pdf_file_path, "application/pdf", 1, "utf-8"
        )
        uploaded_file.write(pdf_file.read())
        uploaded_file.seek(0)

        response = client.post(
            url, {"files[]": uploaded_file}, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        # The response was successful.
        assert 200 == response.status_code
        assert "doc" in response.context
        expected_file_name = pdf_file_path.split("/")[-1]
        assert expected_file_name == response.context["doc"].title
        pdf_file.seek(0)
        assert len(pdf_file.read()) == response.context["doc"].file_size
        # Verify that the HIPDocument was created.
        document = get_document_model().objects.get(title=expected_file_name)
        assert document.collection == Collection.get_first_root_node()


@pytest.mark.parametrize("next_url", ["", "next_url"])
def test_wagtail_login_redirects_to_cms_and_admin_login_get(db, client, next_url):
    """Attempting to GET the Wagtail login redirects the user to the cms_and_admin_login view."""
    url = reverse("wagtailadmin_login")
    if next_url:
        url += f"?next={next_url}"
    response = client.get(url)
    # The user is redirected to the regular login page, and the 'next' parameter
    # persists to the regular login page.
    assert 302 == response.status_code
    assert f"{reverse('login')}?next={next_url}" == response.url


@pytest.mark.parametrize("next_url", ["", "next_url"])
def test_wagtail_login_redirects_to_cms_and_admin_login_post(db, client, next_url):
    """Attempting to POST to Wagtail login redirects user to cms_and_admin_login view."""
    user = UserFactory(email="test-user")
    user.set_password("testpassword1")
    user.save()

    url = reverse("wagtailadmin_login")
    if next_url:
        url += f"?next={next_url}"

    response = client.post(url, {"username": user.email, "password": "testpassword1"})

    # The user is redirected to the regular login page, and the 'next' parameter
    # persists to the regular login page.
    assert 302 == response.status_code
    assert f"{reverse('login')}?next={next_url}" == response.url


@pytest.mark.parametrize("next_url", ["", "next_url"])
def test_djangoadmin_login_redirects_to_cms_and_admin_login_get(db, client, next_url):
    """Attempting to GET Django admin login redirects user to cms_and_admin_login view."""
    url = reverse("admin:login")
    if next_url:
        url += f"?next={next_url}"
    response = client.get(url)
    # The user is redirected to the regular login page, and the 'next' parameter
    # persists to the regular login page.
    assert 302 == response.status_code
    assert f"{reverse('login')}?next={next_url}" == response.url


@pytest.mark.parametrize("next_url", ["", "next_url"])
def test_djangoadmin_login_redirects_to_cms_and_admin_login_post(db, client, next_url):
    """Attempting to POST to Django admin login redirects user to cms_and_admin_login view."""
    user = UserFactory(email="test-user")
    user.set_password("testpassword1")
    user.save()

    url = reverse("admin:login")
    if next_url:
        url += f"?next={next_url}"

    response = client.post(url, {"username": user.email, "password": "testpassword1"})

    # The user is redirected to the regular login page, and the 'next' parameter
    # persists to the regular login page.
    assert 302 == response.status_code
    assert f"{reverse('login')}?next={next_url}" == response.url


def test_get_document_success(db, client):
    """Sending valid parameters should return the expected document."""
    document = DocumentFactory()
    url = reverse(
        "get_document",
        kwargs={"document_id": document.id, "document_name": document.filename},
    )
    response = client.get(url)
    assert response.status_code == 200
    assert (
        response.headers.get("Content-Disposition")
        == f'inline; filename="{document.filename}"'
    )


def test_get_document_no_parameters(db, client):
    """Sending no parameters to the get_document view returns a 404 error."""
    document = DocumentFactory()
    # Create a URL without the document_id and document_name parameters.
    url = reverse(
        "get_document",
        kwargs={"document_id": document.id, "document_name": document.filename},
    )
    url = url.replace(f"{document.id}/", "").replace(f"{document.filename}/", "")
    response = client.get(url)
    assert response.status_code == 404


def test_get_document_non_existent_parameters(db, client):
    """Sending non-existent parameter values, like id=1000000000, returns a 404 error."""
    document = DocumentFactory()
    # A URL with a document_id that doesn't exist.
    url = reverse(
        "get_document",
        kwargs={"document_id": 1_000_000_000, "document_name": document.filename},
    )

    response = client.get(url)
    assert response.status_code == 404


def test_get_document_non_matching_parameters(db, client):
    """Sending parameters that don't match returns a 404 error."""
    document1 = DocumentFactory()
    document2 = DocumentFactory()
    # A URL with the id of document1 and name of document2.
    url = reverse(
        "get_document",
        kwargs={"document_id": document1.id, "document_name": document2.filename},
    )

    response = client.get(url)
    assert response.status_code == 404

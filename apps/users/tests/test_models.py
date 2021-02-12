import pytest
from apps.users.tests.factories import DEFAULT_PASSWORD, UserFactory


pytestmark = pytest.mark.django_db


def test_user_get_full_name():
    user = UserFactory()
    assert user.get_full_name() == f"{user.first_name} {user.last_name}"


def test_user_get_full_name_if_first_name_empty():
    user = UserFactory(first_name="")
    assert user.get_full_name() == user.last_name


def test_user_get_full_name_if_last_name_empty():
    user = UserFactory(first_name="", last_name="")
    assert user.get_full_name() == user.first_name


def test_user_get_full_name_if_name_fields_empty():
    user = UserFactory(first_name="", last_name="")
    assert user.get_full_name() == ""


def test_user_get_short_name():
    user = UserFactory()
    assert user.get_short_name() == user.first_name


def test_str_method():
    user = UserFactory()
    assert str(user) == user.email


def test_superuser():
    user = UserFactory(is_superuser=True)
    assert user.is_superuser


def test_case_insensitive_login(client):
    mixed_case_email = "Mixed.Case@example.com"
    user = UserFactory(email=mixed_case_email)
    # lowercase the email and they should be able to login
    assert client.login(email=mixed_case_email.lower(), password=DEFAULT_PASSWORD)

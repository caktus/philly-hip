import pytest
from apps.users.tests.factories import DEFAULT_PASSWORD, UserFactory


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def superuser(db):
    return UserFactory(is_superuser=True)


def test_user_get_full_name(user):
    assert user.get_full_name() == f"{user.first_name} {user.last_name}"


def test_user_get_full_name_if_first_name_empty(user):
    user.first_name = ""
    assert user.get_full_name() == user.last_name


def test_user_get_full_name_if_last_name_empty(user):
    user.last_name = ""
    assert user.get_full_name() == user.first_name


def test_user_get_full_name_if_name_fields_empty(user):
    user.first_name = user.last_name = ""
    assert user.get_full_name() == ""


def test_user_get_short_name(user):
    assert user.get_short_name() == user.first_name


def test_str_method(user):
    assert str(user) == user.email


def test_superuser(superuser):
    assert superuser.is_superuser


def test_case_insensitive_login(client, user):
    mixed_case_email = "Mixed.Case@example.com"
    user.email = mixed_case_email
    user.save()
    # lowercase the email and they should be able to login
    assert client.login(email=mixed_case_email.lower(), password=DEFAULT_PASSWORD)

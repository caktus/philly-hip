from apps.users.tests.factories import DEFAULT_PASSWORD, UserFactory
from pytest_factoryboy import register


register(UserFactory)


def test_user_get_full_name(db, user):
    assert user.get_full_name() == f"{user.first_name} {user.last_name}"


def test_user_get_full_name_if_first_name_empty(db, user):
    user.first_name = ""
    assert user.get_full_name() == user.last_name


def test_user_get_full_name_if_last_name_empty(db, user):
    user.last_name = ""
    assert user.get_full_name() == user.first_name


def test_user_get_full_name_if_name_fields_empty(db, user):
    user.first_name = user.last_name = ""
    assert user.get_full_name() == ""


def test_user_get_short_name(db, user):
    assert user.get_short_name() == user.first_name


def test_str_method(db, user):
    assert str(user) == user.email


def test_superuser(db, user_factory):
    superuser = user_factory(is_superuser=True)
    assert superuser.is_superuser


def test_case_insensitive_login(client, db, user):
    mixed_case_email = "Mixed.Case@example.com"
    user.email = mixed_case_email
    user.save()
    # lowercase the email and they should be able to login
    assert client.login(email=mixed_case_email.lower(), password=DEFAULT_PASSWORD)

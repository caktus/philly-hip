from django.db import IntegrityError

import pytest
from pytest_factoryboy import register

from apps.users.tests.factories import DEFAULT_PASSWORD, UserFactory


# This registers User as a fixture (defaults to lowercase-underscored representation of
# the factory's Meta.model attribute). It also registers user_factory as a fixture, but
# we currently don't use that in this test file.
register(UserFactory)
# This registers another fixture, names it explicitly "superuser" and passes a kwarg to
# the factory to customize the instance returned. NOTE: the kwarg you provide must be
# specified in the factory class and not just only in the underlying Django model class,
# so I had to explicitly add a `is_superuser` attribute to UserFactory.
register(UserFactory, "superuser", is_superuser=True)


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


def test_superuser(db, superuser):
    assert superuser.is_superuser is True


def test_case_insensitive_login(client, db, user):
    mixed_case_email = "Mixed.Case@example.com"
    user.email = mixed_case_email
    user.save()
    # lowercase the email and they should be able to login
    assert client.login(email=mixed_case_email.lower(), password=DEFAULT_PASSWORD)


@pytest.mark.django_db
def test_email_case_insensitive_unique():
    UserFactory(email="Caktus@example.com")
    msg = 'duplicate key value violates unique constraint "users_user_email_key"'

    with pytest.raises(IntegrityError, match=msg):
        UserFactory(email="caktus@example.com")

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import CIEmailField
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import IndexedTimeStampedModel
from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, IndexedTimeStampedModel):
    # Support for CIEmailField will be depreacated after Django 4.2 in favor
    # of EmailField. Below is how to migrate to the vanilla EmailField Whilst
    # creating a non-deterministic collation. Can't migrate yet because it requires
    # Postgres 12 or higher. Currently Hip Philly is running Postgres 11.
    # https://adamj.eu/tech/2023/02/23/migrate-django-postgresql-ci-fields-case-insensitive-collation/
    email = CIEmailField(max_length=255, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.get_username()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

import factory


DEFAULT_PASSWORD = "mypasswordisbad"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.faker.Faker("email")
    first_name = factory.faker.Faker("first_name")
    last_name = factory.faker.Faker("last_name")
    password = DEFAULT_PASSWORD
    is_superuser = False

    # From factory boy docs
    # https://factoryboy.readthedocs.io/en/stable/recipes.html#custom-manager-methods
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        if kwargs.pop("is_superuser", False):
            return manager.create_superuser(*args, **kwargs)
        return manager.create_user(*args, **kwargs)


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.faker.Faker("company")

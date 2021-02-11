from django.contrib.auth import get_user_model

import factory


DEFAULT_PASSWORD = "mypasswordisbad"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.faker.Faker("email")
    password = DEFAULT_PASSWORD

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

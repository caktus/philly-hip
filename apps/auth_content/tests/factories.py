import random

import factory
import wagtail_factories

from apps.users.tests.factories import UserFactory

from ..models import (
    BigCitiesHomePage,
    ClosedPODChildPage,
    ClosedPODContactInformation,
    ClosedPODHomePage,
    PCWMSAHomePage,
)


class ClosedPODHomePageFactory(wagtail_factories.PageFactory):
    action_section = factory.faker.Faker("text")

    class Meta:
        model = ClosedPODHomePage


class ClosedPODChildPageFactory(wagtail_factories.PageFactory):
    description = factory.faker.Faker("text")

    class Meta:
        model = ClosedPODChildPage


class PCWMSAHomePageFactory(wagtail_factories.PageFactory):
    subtitle = factory.faker.Faker("text")
    action_section = factory.faker.Faker("text")

    class Meta:
        model = PCWMSAHomePage


class BigCitiesHomePageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("text")

    class Meta:
        model = BigCitiesHomePage


class ClosedPODContactInformationFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    facility_name = factory.faker.Faker("text")
    facility_id = factory.faker.Faker("word")
    phone_number = factory.faker.Faker("phone_number")
    extension = random.randrange(0, 9999)
    available_24_7 = random.choice([True, False])
    special_instructions = factory.faker.Faker("text")

    primary_contact_name = factory.faker.Faker("name")
    primary_contact_work_email = factory.faker.Faker("email")
    primary_contact_personal_email = factory.faker.Faker("email")
    primary_contact_cell_phone = factory.faker.Faker("phone_number")
    primary_contact_cell_phone_provider = random.choice(
        ["AT&T", "Verizon", "T-Mobile", "Dish", "Other"]
    )

    secondary_contact_name = factory.faker.Faker("name")
    secondary_contact_work_email = factory.faker.Faker("email")
    secondary_contact_personal_email = factory.faker.Faker("email")
    secondary_contact_cell_phone = factory.faker.Faker("phone_number")
    secondary_contact_cell_phone_provider = random.choice(
        ["AT&T", "Verizon", "T-Mobile", "Dish", "Other"]
    )

    class Meta:
        model = ClosedPODContactInformation

import random

import factory

from ..models import (
    CodeRedCodeBlueSubscriber,
    CommunityResponseSubscriber,
    DrugOverdoseSubscriber,
    InternalEmployeeAlertSubscriber,
    PublicHealthPreparednessSubscriber,
)


class CodeRedCodeBlueSubscriberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CodeRedCodeBlueSubscriber

    first_name = factory.faker.Faker("first_name")
    last_name = factory.faker.Faker("last_name")
    agency_name = factory.faker.Faker("company")
    work_phone = factory.faker.Faker("phone_number")
    work_email = factory.faker.Faker("email")
    cell_phone = factory.faker.Faker("phone_number")
    personal_email = factory.faker.Faker("email")


class CommunityResponseSubscriberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommunityResponseSubscriber

    first_name = factory.faker.Faker("first_name")
    last_name = factory.faker.Faker("last_name")
    email_address = factory.faker.Faker("email")
    cell_phone = factory.faker.Faker("phone_number")
    organization_name = factory.faker.Faker("company")
    organization_zip_code = factory.faker.Faker("postcode")
    organization_type = random.choice(
        [str(t) for t in CommunityResponseSubscriber.ORGANIZATION_TYPE_CHOICES]
    )
    organization_community_members_served = random.choice(
        [str(l) for l in CommunityResponseSubscriber.COMMUNITY_MEMBERS_CHOICES]
    )
    organization_mission_statement = factory.faker.Faker("text")


class InternalEmployeeAlertSubscriberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InternalEmployeeAlertSubscriber

    first_name = factory.faker.Faker("first_name")
    last_name = factory.faker.Faker("last_name")
    professional_license = random.choice(
        [str(l) for l in InternalEmployeeAlertSubscriber.PROFESSIONAL_LICENSE_CHOICES]
    )
    languages_spoken = factory.faker.Faker("word")
    division = random.choice(
        [str(d) for d in InternalEmployeeAlertSubscriber.DIVISION_CHOICES]
    )
    work_phone = factory.faker.Faker("phone_number")
    work_email = factory.faker.Faker("email")
    cell_phone = factory.faker.Faker("phone_number")
    personal_email = factory.faker.Faker("email")
    home_phone = factory.faker.Faker("phone_number")
    street_address = factory.faker.Faker("street_address")
    city = factory.faker.Faker("city")
    state = factory.faker.Faker("state")
    zip_code = factory.faker.Faker("postcode")


class DrugOverdoseSubscriberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DrugOverdoseSubscriber

    first_name = factory.faker.Faker("first_name")
    last_name = factory.faker.Faker("last_name")
    medical_specialty = factory.faker.Faker("word")
    company_name = factory.faker.Faker("company")
    title = factory.faker.Faker("job")
    work_phone = factory.faker.Faker("phone_number")
    notification_group = random.choice(
        [str(n) for n in DrugOverdoseSubscriber.NOTIFICATION_GROUP_CHOICES]
    )
    email_address = factory.faker.Faker("email")
    mobile_phone = factory.faker.Faker("phone_number")


class PublicHealthPreparednessSubscriberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PublicHealthPreparednessSubscriber

    first_name = factory.faker.Faker("first_name")
    last_name = factory.faker.Faker("last_name")
    phone_number = factory.faker.Faker("phone_number")
    email_address = factory.faker.Faker("email")
    organization_name = factory.faker.Faker("company")
    organization_zip_code = factory.faker.Faker("postcode")
    outreach_request_choice = random.choice(
        [str(n) for n in PublicHealthPreparednessSubscriber.OUTREACH_REQUEST_CHOICES]
    )
    outreach_request_additional_info = factory.faker.Faker("text")

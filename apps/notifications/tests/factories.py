import random

import factory

from ..models import InternalEmployeeAlertSubscriber


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

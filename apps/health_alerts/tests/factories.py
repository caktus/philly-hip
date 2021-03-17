import factory
from factory import fuzzy

from ..constants import AGENCY_TYPE_CHOICES
from ..models import HealthAlertSubscriber


class HealthAlertSubscriberFactories(factory.DjangoModelFactory):
    personal_first_name = factory.faker.Faker("first_name")
    personal_last_name = factory.faker.Faker("last_name")
    personal_medical_expertise = factory.faker.Faker("first_name")
    personal_professional_license = factory.Sequence(lambda n: "%07d" % n)
    agency_name = factory.faker.Faker("company")
    agency_type = fuzzy.FuzzyChoice(AGENCY_TYPE_CHOICES)
    agency_zip_code = factory.Sequence(lambda n: "%05d" % n)
    agency_position = factory.faker.Faker("text")
    agency_work_phone = network_fax = factory.Sequence(lambda n: "(123) 222-%04d" % n)
    network_email = factory.Sequence(lambda n: "yoda%04d@gmail.com" % n)
    network_fax = factory.Sequence(lambda n: "(123) 555-%04d" % n)

    class Meta:
        model = HealthAlertSubscriber

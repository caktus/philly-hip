import factory
import wagtail_factories

from ..models import EmergencyResponsePage


class EmergencyResponsePageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("sentence")
    description = factory.faker.Faker("text")

    class Meta:
        model = EmergencyResponsePage

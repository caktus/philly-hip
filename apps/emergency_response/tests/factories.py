import factory
import wagtail_factories

from ..models import EmergencyResponsePage, HeatIndexPage, VolunteerPage


class EmergencyResponsePageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("sentence")
    description = factory.faker.Faker("text")

    class Meta:
        model = EmergencyResponsePage


class HeatIndexPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = HeatIndexPage


class VolunteerPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = VolunteerPage

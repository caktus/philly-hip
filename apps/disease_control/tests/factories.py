import factory
import wagtail_factories

from ..models import DiseasePage, EmergentHealthTopicsPage


class DiseasePageFactory(wagtail_factories.PageFactory):
    description = factory.faker.Faker("text")

    class Meta:
        model = DiseasePage


class EmergentHealthTopicsPageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("sentence")

    class Meta:
        model = EmergentHealthTopicsPage

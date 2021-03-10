import factory
import wagtail_factories

from ..models import DiseaseAndConditionDetailPage, EmergentHealthTopicsPage


class DiseaseAndConditionDetailPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = DiseaseAndConditionDetailPage


class EmergentHealthTopicsPageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("sentence")

    class Meta:
        model = EmergentHealthTopicsPage

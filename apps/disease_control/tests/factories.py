import factory
import wagtail_factories

from ..models import DiseaseAndConditionDetailPage, EmergentHealthTopicListPage


class DiseaseAndConditionDetailPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = DiseaseAndConditionDetailPage


class EmergentHealthTopicListPageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("sentence")

    class Meta:
        model = EmergentHealthTopicListPage

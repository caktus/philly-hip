import factory
import wagtail_factories

from apps.disease_control import models


class DiseaseControlListPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.DiseaseControlListPage


class DiseaseControlPageFactory(wagtail_factories.PageFactory):
    page_type = 1

    class Meta:
        model = models.DiseaseControlPage


class DiseaseAndConditionListPageFactory(wagtail_factories.PageFactory):
    page_type = 3

    class Meta:
        model = models.DiseaseAndConditionListPage


class DiseaseAndConditionDetailPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.DiseaseAndConditionDetailPage


class EmergentHealthTopicListPageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("sentence")

    class Meta:
        model = models.EmergentHealthTopicListPage

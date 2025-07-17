from django.core.management import call_command

import factory
import wagtail_factories

from apps.disease_control import models


class PageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = None

    @factory.post_generation
    def set_initial_value(obj, create, extracted, **kwargs):
        if create:
            call_command("update_index")


class DiseaseControlListPageFactory(PageFactory):
    class Meta:
        model = models.DiseaseControlListPage


class DiseaseControlPageFactory(PageFactory):
    page_type = 1

    class Meta:
        model = models.DiseaseControlPage


class DiseaseAndConditionListPageFactory(PageFactory):
    page_type = 3

    class Meta:
        model = models.DiseaseAndConditionListPage


class DiseaseAndConditionDetailPageFactory(PageFactory):
    class Meta:
        model = models.DiseaseAndConditionDetailPage


class EmergentHealthTopicListPageFactory(PageFactory):
    title = factory.faker.Faker("sentence")

    class Meta:
        model = models.EmergentHealthTopicListPage

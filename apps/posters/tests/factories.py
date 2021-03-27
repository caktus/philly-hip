import factory
import wagtail_factories

from ..models import PosterCategory, PosterDetailPage, PosterListPage


class PosterCategoryFactory(factory.django.DjangoModelFactory):
    name = factory.faker.Faker("word")

    class Meta:
        model = PosterCategory


class PosterDetailPageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("sentence")
    main_poster = factory.SubFactory(wagtail_factories.factories.DocumentFactory)
    thumbnail = factory.SubFactory(wagtail_factories.factories.ImageFactory)
    category = factory.SubFactory(PosterCategoryFactory)
    disease = factory.SubFactory(
        "apps.disease_control.tests.factories.DiseaseAndConditionDetailPageFactory"
    )

    class Meta:
        model = PosterDetailPage


class PosterListPageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("sentence")

    class Meta:
        model = PosterListPage

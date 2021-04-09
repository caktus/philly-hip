import factory
import wagtail_factories


from ..models import (  # isort: skip
    BigCitiesHomePage,
    ClosedPODChildPage,
    ClosedPODHomePage,
    PCWMSAHomePage,
)


class ClosedPODHomePageFactory(wagtail_factories.PageFactory):
    action_section = factory.faker.Faker("text")

    class Meta:
        model = ClosedPODHomePage


class ClosedPODChildPageFactory(wagtail_factories.PageFactory):
    description = factory.faker.Faker("text")

    class Meta:
        model = ClosedPODChildPage


class PCWMSAHomePageFactory(wagtail_factories.PageFactory):
    subtitle = factory.faker.Faker("text")
    action_section = factory.faker.Faker("text")

    class Meta:
        model = PCWMSAHomePage


class BigCitiesHomePageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("text")

    class Meta:
        model = BigCitiesHomePage

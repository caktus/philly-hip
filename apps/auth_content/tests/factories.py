import factory
import wagtail_factories

from ..models import ClosedPODChildPage, ClosedPODHomePage


class ClosedPODHomePageFactory(wagtail_factories.PageFactory):
    action_section = factory.faker.Faker("text")

    class Meta:
        model = ClosedPODHomePage


class ClosedPODChildPageFactory(wagtail_factories.PageFactory):
    description = factory.faker.Faker("text")

    class Meta:
        model = ClosedPODChildPage

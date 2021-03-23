import factory
import wagtail_factories

from ..models import ClosedPODHomePage


class ClosedPODHomePageFactory(wagtail_factories.PageFactory):
    action_section = factory.faker.Faker("text")

    class Meta:
        model = ClosedPODHomePage

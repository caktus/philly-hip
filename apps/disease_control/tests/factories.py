import factory
import wagtail_factories

from ..models import DiseasePage


class DiseasePageFactory(wagtail_factories.PageFactory):
    description = factory.faker.Faker("text")

    class Meta:
        model = DiseasePage

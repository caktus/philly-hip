import wagtail_factories

from ..models import DiseasePage


class DiseasePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = DiseasePage

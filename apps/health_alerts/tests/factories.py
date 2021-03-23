import random

import wagtail_factories

from ..models import HealthAlertDetailPage, HealthAlertListPage


class HealthAlertDetailPageFactory(wagtail_factories.PageFactory):
    priority = random.choice([1, 2, 3, 4])

    class Meta:
        model = HealthAlertDetailPage


class HealthAlertListPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = HealthAlertListPage

import random

import factory
import wagtail_factories

from .. import models


class ExternalReportBlockFactory(wagtail_factories.StructBlockFactory):
    title = "title here"
    url = factory.faker.Faker("url")
    update_frequency = random.choice(
        ["Annually", "Warterly", "Monthly", "Weekly", "all the time!!!"]
    )
    last_updated = factory.faker.Faker("date")

    class Meta:
        model = models.ExternalReportBlock


class DataReportListPageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("sentence")
    external_reports = wagtail_factories.StreamFieldFactory(
        {"external_reports": ExternalReportBlockFactory}
    )

    class Meta:
        model = models.DataReportListPage


class DataReportDetailPageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("sentence")

    class Meta:
        model = models.DataReportDetailPage


class DataReportDetailArchiveListPageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("sentence")

    class Meta:
        model = models.DataReportDetailArchiveListPage


class DataReportDetailArchiveDetailPageFactory(wagtail_factories.PageFactory):
    title = factory.faker.Faker("sentence")
    year = random.randrange(2000, 2021)

    class Meta:
        model = models.DataReportDetailArchiveDetailPage

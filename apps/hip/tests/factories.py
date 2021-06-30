from django.utils.timezone import now

import factory
import wagtail_factories
from wagtail.documents import get_document_model

from ..models import HomePage, ListPage, StaticPage


class TextOrTableStreamBlockFactory(wagtail_factories.StructBlockFactory):
    rich_text = factory.faker.Faker("text")


class StreamAndNavHeadingBlockFactory(wagtail_factories.StructBlockFactory):
    nav_heading = factory.faker.Faker("text")
    is_card = True
    body = factory.SubFactory(TextOrTableStreamBlockFactory)


class QuickLinkCardFactory(wagtail_factories.StructBlockFactory):
    title = factory.faker.Faker("text")
    link_url = factory.faker.Faker("url")
    title = factory.faker.Faker("text")


class StaticPageFactory(wagtail_factories.PageFactory):
    body = wagtail_factories.StreamFieldFactory(
        {"section": StreamAndNavHeadingBlockFactory()}
    )
    latest_revision_created_at = now()

    class Meta:
        model = StaticPage


class HomePageFactory(wagtail_factories.PageFactory):
    about = factory.faker.Faker("text")
    quick_links = wagtail_factories.StreamFieldFactory(
        {"quick_links": StreamAndNavHeadingBlockFactory()}
    )

    class Meta:
        model = HomePage


class ListRowBlockFactory(wagtail_factories.StructBlockFactory):
    description = factory.faker.Faker("text")
    page = factory.SubFactory(StaticPageFactory)


class ListRowStreamBlockFactory(wagtail_factories.StructBlockFactory):
    rows = factory.SubFactory(ListRowBlockFactory)


class ListSectionBlockFactory(wagtail_factories.StructBlockFactory):
    header = factory.faker.Faker("text")
    is_card = True
    rows = factory.SubFactory(ListRowStreamBlockFactory)


class ListPageFactory(wagtail_factories.PageFactory):
    list_section = wagtail_factories.StreamFieldFactory(
        {"list_section": StreamAndNavHeadingBlockFactory()}
    )
    latest_revision_created_at = now()

    class Meta:
        model = ListPage


class DocumentFactory(factory.django.DjangoModelFactory):
    title = "A document title"
    file = factory.django.FileField(filename="fake.pdf")

    class Meta:
        model = get_document_model()

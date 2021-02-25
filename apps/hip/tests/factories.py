from django.utils.timezone import now

import factory
import wagtail_factories

from ..models import HomePage, StaticPage


class TextOrTableStreamBlockFactory(wagtail_factories.StructBlockFactory):
    rich_text = factory.faker.Faker("text")


class StreamAndNavHeadingBlockFactory(wagtail_factories.StructBlockFactory):
    nav_heading = factory.faker.Faker("text")
    is_card = True
    body = factory.SubFactory(TextOrTableStreamBlockFactory)


class QuickLinkCardFactory(wagtail_factories.StructBlockFactory):
    title = factory.faker.Faker("text")
    link_url = factory.faker.Faker("url")


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
        {"quick_links": QuickLinkCardFactory}
    )

    class Meta:
        model = HomePage

from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from ..common.models import IndexedTimeStampedModel


@register_snippet
class Contact(IndexedTimeStampedModel):
    business_hours_call_number = PhoneNumberField(
        help_text="Business Hours Call Number",
    )
    business_hours_fax_number = PhoneNumberField(
        help_text="Business Hours Fax Number",
    )
    after_hours_call_number = PhoneNumberField(
        help_text="After Hours Call Number",
    )

    panels = [
        FieldPanel("business_hours_call_number"),
        FieldPanel("business_hours_fax_number"),
        FieldPanel("after_hours_call_number"),
    ]

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return f'Contact Us - Created: {self.created.strftime("%b %d %Y %H:%M:%S")}'


class TableRow(blocks.StructBlock):
    column_1 = blocks.RichTextBlock(
        max_length=255,
        required=False,
        help_text=("Text for column 1"),
    )
    column_2 = blocks.RichTextBlock(
        max_length=255,
        required=False,
        help_text=("Text for column 2"),
    )

    class Meta:
        label = "Table row"
        form_classname = "two-column-table__row"


class TableRowStreamBlock(blocks.StreamBlock):
    rows = TableRow()


class TwoColumnBlock(blocks.StructBlock):
    has_grid_pattern = blocks.BooleanBlock(
        required=False, help_text="Does this table's styling have a grid pattern?"
    )
    is_first_row_header = blocks.BooleanBlock(
        required=False, help_text="Should the first row be displayed as a header?"
    )
    rows = TableRowStreamBlock()

    class Meta:
        template = "hip/text_or_table_stream.html"


class TextOrTableStreamBlock(blocks.StreamBlock):
    rich_text = blocks.RichTextBlock()
    two_column_table = TwoColumnBlock()


class StreamAndNavHeadingBlock(blocks.StructBlock):
    """
    A Block with a navigation heading and a StreamBlock.

    If a page has a scrolling navigation that links to each section of the page,
    the navigation will need to have a heading for each section of the page. The
    heading can be defined in the nav_heading block.
    """

    nav_heading = blocks.CharBlock(
        max_length=80,
        required=False,
        help_text=(
            "The heading that should appear for this section in the scrolling "
            "navigation on the side of the page."
        ),
    )
    is_card = blocks.BooleanBlock(
        required=False, help_text=("Is this content block a card?")
    )
    body = TextOrTableStreamBlock()
    contact_info = SnippetChooserBlock(Contact, required=False)


class StaticPage(Page):
    """A Page with only sections of static content."""

    body = StreamField(
        [
            ("section", StreamAndNavHeadingBlock()),
        ]
    )

    content_panels = [
        FieldPanel("title"),
        StreamFieldPanel("body"),
    ]
    promote_panels = [
        FieldPanel("slug"),
    ]

    def get_context(self, request):
        """
        Add the HTTP_REFERER to the context so that we can show a back button.
        """
        from apps.common.utils import get_home_page_url

        context = super().get_context(request)

        # Use the HTTP_REFERER, or default to the value returned by get_home_page_url().
        # Note: we use the try/except logic here (rather than request.META.get...)
        # in order to avoid calling get_home_page_url() every time.
        try:
            context["prev_url"] = request.META["HTTP_REFERER"]
        except KeyError:
            context["prev_url"] = get_home_page_url()

        # right nav uses the `nav_heading` variable in the template to create links
        right_nav_headings = []
        for block in self.body:
            if block.value["nav_heading"]:
                right_nav_headings.append(block.value["nav_heading"])
        context["right_nav_headings"] = right_nav_headings

        return context


class QuickLinkStructValue(blocks.StructValue):
    def link(self):
        """Determine the link based on "link_page" or "link_url"."""
        if self.get("link_page", None):
            return self["link_page"].url
        else:
            return self.get("link_url", None)

    def updated_date(self):
        """Return updated date based on either "link_page" or "updated_on"."""
        # If the link_page is not None, then use its latest_revision_created_at.
        if self.get("link_page", None):
            return self["link_page"].latest_revision_created_at.date()
        else:
            return self.get("updated_on", "")


class QuickLinkCard(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=80,
        required=True,
        help_text=("The linked text that will be visible to the reader"),
    )
    link_page = blocks.PageChooserBlock(
        required=False,
        help_text=("An internal page"),
    )
    link_url = blocks.URLBlock(
        max_length=255,
        required=False,
        help_text=("An external URL (if not linking to an internal page)"),
    )
    updated_on = blocks.DateBlock(
        required=False,
        help_text=(
            "If the link is to an external URL, this will be the displayed as the "
            "updated date"
        ),
    )

    class Meta:
        value_class = QuickLinkStructValue


class HomePage(Page):
    quick_links = StreamField(
        [
            ("quick_links", QuickLinkCard()),
        ],
        blank=True,
    )
    about = RichTextField(blank=True)
    contact_info = models.ForeignKey(
        "Contact", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    content_panels = [
        FieldPanel("title"),
        SnippetChooserPanel("contact_info"),
        StreamFieldPanel("quick_links"),
        FieldPanel("about"),
    ]

    def get_context(self, request):
        """Add recent_updates to context."""
        from .utils import get_most_recent_objects

        context = super().get_context(request)
        context["recent_updates"] = get_most_recent_objects(object_count=10)
        return context

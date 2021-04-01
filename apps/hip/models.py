from django.db import models
from django.utils.timezone import localtime

from phonenumber_field.modelfields import PhoneNumberField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from apps.common.models import HipBasePage, IndexedTimeStampedModel


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


class ThreeColumnTableRow(blocks.StructBlock):
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
    column_3 = blocks.RichTextBlock(
        max_length=255,
        required=False,
        help_text=("Text for column 3"),
    )

    class Meta:
        label = "Table row"
        form_classname = "three-column-table__row"


class ThreeColumnTableRowStreamBlock(blocks.StreamBlock):
    rows = ThreeColumnTableRow()


class ThreeColumnBlock(blocks.StructBlock):
    has_grid_pattern = blocks.BooleanBlock(
        required=False, help_text="Does this table's styling have a grid pattern?"
    )
    is_first_row_header = blocks.BooleanBlock(
        required=False, help_text="Should the first row be displayed as a header?"
    )
    rows = ThreeColumnTableRowStreamBlock()

    class Meta:
        template = "hip/text_or_table_stream.html"


class FourColumnTableRow(blocks.StructBlock):
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
    column_3 = blocks.RichTextBlock(
        max_length=255,
        required=False,
        help_text=("Text for column 3"),
    )
    column_4 = blocks.RichTextBlock(
        max_length=255,
        required=False,
        help_text=("Text for column 4"),
    )

    class Meta:
        label = "Table row"
        form_classname = "four-column-table__row"


class FourColumnTableRowStreamBlock(blocks.StreamBlock):
    rows = FourColumnTableRow()


class FourColumnBlock(blocks.StructBlock):
    has_grid_pattern = blocks.BooleanBlock(
        required=False, help_text="Does this table's styling have a grid pattern?"
    )
    is_first_row_header = blocks.BooleanBlock(
        required=False, help_text="Should the first row be displayed as a header?"
    )
    rows = FourColumnTableRowStreamBlock()

    class Meta:
        template = "hip/text_or_table_stream.html"


class TextOrTableStreamBlock(blocks.StreamBlock):
    rich_text = blocks.RichTextBlock()
    two_column_table = TwoColumnBlock()
    three_column_table = ThreeColumnBlock()
    four_column_table = FourColumnBlock()


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


class StaticPage(HipBasePage):
    """A Page with only sections of static content."""

    subpage_types = []

    body = StreamField(
        [
            ("section", StreamAndNavHeadingBlock()),
        ]
    )

    content_panels = HipBasePage.content_panels + [
        StreamFieldPanel("body"),
    ]
    promote_panels = [
        FieldPanel("slug"),
    ]
    search_fields = HipBasePage.search_fields + [
        index.SearchField("body"),
    ]

    def get_context(self, request):
        """
        Add the HTTP_REFERER to the context so that we can show a back button.
        """
        context = super().get_context(request)

        # right nav uses the `nav_heading` variable in the template to create links
        right_nav_headings = []
        for block in self.body:
            if block.value["nav_heading"]:
                right_nav_headings.append(block.value["nav_heading"])
        context["right_nav_headings"] = right_nav_headings

        return context


class ListRowBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock(
        required=True,
        help_text=("An internal page"),
    )
    description = blocks.RichTextBlock(
        required=False,
        help_text=("Description for this row"),
    )


class ListRowStreamBlock(blocks.StreamBlock):
    rows = ListRowBlock()


class ListSectionBlock(blocks.StructBlock):
    header = blocks.CharBlock(
        max_length=80,
        required=False,
        help_text=("The heading for this section of rows (maximum of 80 characters)."),
    )
    show_header_in_right_nav = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text="Should this header be shown in the navigation on the right side of the page?",
    )
    rows = ListRowStreamBlock()


class ListPage(HipBasePage):
    show_breadcrumb = models.BooleanField(
        default=False,
        blank=True,
        help_text="Should this page show a breadcrumb at the top of the page?",
    )
    show_right_nav = models.BooleanField(
        default=False,
        blank=True,
        help_text="Should this page show a navigation of its sections on the right side of the page?",
    )
    list_section = StreamField(
        [
            ("list_section", ListSectionBlock()),
        ]
    )

    content_panels = HipBasePage.content_panels + [
        FieldPanel("show_breadcrumb"),
        FieldPanel("show_right_nav"),
        StreamFieldPanel("list_section"),
    ]
    promote_panels = [FieldPanel("slug")]
    search_fields = HipBasePage.search_fields + [
        index.SearchField("list_section"),
    ]

    def get_context(self, request):
        """Add headings for the right nav section to the context."""
        context = super().get_context(request)

        right_nav_headings = []
        for block in self.list_section:
            if block.value["show_header_in_right_nav"]:
                right_nav_headings.append(block.value["header"])
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
        # If the link_page is not None, then use its latest_revision_created_at's
        # date, in the project's time zone.
        if self.get("link_page", None):
            return localtime(self["link_page"].latest_revision_created_at).date()
        else:
            return self.get("updated_on", "")


class QuickLinkCard(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=80,
        required=True,
        help_text=(
            "The linked text that will be visible to the reader (maximum of 80 characters)"
        ),
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


class HomePage(HipBasePage):
    max_count = 1
    short_description = models.CharField(
        max_length=255,
        default="",
        blank=True,
        help_text=(
            "A short description of the website that will be shown to users when they are on the home page."
        ),
    )
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

    content_panels = HipBasePage.content_panels + [
        FieldPanel("short_description"),
        SnippetChooserPanel("contact_info"),
        StreamFieldPanel("quick_links"),
        FieldPanel("about"),
    ]

    search_fields = HipBasePage.search_fields + [
        index.SearchField("quick_links"),
        index.SearchField("about"),
    ]

    def get_context(self, request):
        """Add recent_updates to context."""
        from .utils import get_most_recent_objects

        context = super().get_context(request)
        context["recent_updates"] = get_most_recent_objects(object_count=10)
        return context

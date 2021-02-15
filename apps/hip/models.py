from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page


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


class QuickLinkCard(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text=("The linked text that will be visible to the reader"),
    )
    link_url = blocks.URLBlock(
        max_length=255,
        required=True,
        help_text=("The URL to link to"),
    )
    text = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text=("Text below the title "),
    )


class HomePage(Page):
    quick_links = StreamField(
        [
            ("quick_links", QuickLinkCard()),
        ],
        blank=True,
    )
    about = RichTextField(blank=True)

    content_panels = [
        FieldPanel("title"),
        StreamFieldPanel("quick_links"),
        FieldPanel("about"),
    ]

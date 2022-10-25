from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index

from apps.common.models import HipBasePage


class LinkBlock(blocks.StructBlock):
    subtitle = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text="The subtitle for this block of links.",
    )
    text = blocks.RichTextBlock()


class SectionOfLinkBlocks(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text="The title for this section.",
    )
    number_of_columns = blocks.IntegerBlock(
        min_value=1,
        max_value=2,
        default=1,
        help_text="The number of columns in which to show this section.",
    )
    link_blocks = blocks.StreamBlock(
        [
            ("block_of_links", LinkBlock(blank=True)),
        ],
        required=False,
    )


class EmergencyResponsePage(HipBasePage):
    subpage_types = ["hip.StaticPage"]

    description = RichTextField(blank=True)
    action_section = RichTextField(
        blank=True,
        help_text="This section will stand out to users, calling them to perform an action.",
    )
    sections_of_links = StreamField(
        [
            ("section_of_links", SectionOfLinkBlocks()),
        ],
        blank=True,
    )

    content_panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("action_section"),
        FieldPanel("sections_of_links"),
    ]

    search_fields = HipBasePage.search_fields + [
        index.SearchField("description"),
        index.SearchField("action_section"),
        index.SearchField("sections_of_links"),
    ]

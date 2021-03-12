from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page


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


class EmergencyResponsePage(Page):
    subpage_types = [
        "emergency_response.VolunteerPage",
        "emergency_response.HeatIndexPage",
    ]

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
        StreamFieldPanel("sections_of_links"),
    ]


class VolunteerPage(Page):
    parent_page_types = ["emergency_response.EmergencyResponsePage"]
    subpage_types = []

    content_panels = [
        FieldPanel("title"),
    ]


class HeatIndexPage(Page):
    parent_page_types = ["emergency_response.EmergencyResponsePage"]
    subpage_types = []

    content_panels = [
        FieldPanel("title"),
    ]

from django.db import models
from django.shortcuts import reverse
from django.utils.timezone import localtime

from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from phonenumber_field.modelfields import PhoneNumberField
from wagtail import blocks
from wagtail import models as wagtail_models
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.documents.models import Document, DocumentQuerySet
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock
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


@register_snippet
class SocialMedia(IndexedTimeStampedModel):
    org_name = models.CharField("Organization Name", max_length=255)
    twitter = models.URLField(max_length=255, blank=True)
    facebook = models.URLField(max_length=255, blank=True)
    instagram = models.URLField(max_length=255, blank=True)
    youtube = models.URLField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Social Media"
        verbose_name_plural = "Social Media"

    def __str__(self):
        return f"Social Media for {self.org_name}"


@register_snippet
class ButtonSnippet(IndexedTimeStampedModel):
    button_text = models.CharField(max_length=255)
    relative_url = models.CharField(
        max_length=255,
        help_text=(
            "The URL, relative to the domain of this site. For example, /internal-alerts-signup/"
        ),
    )

    def __str__(self):
        return f"Button '{self.button_text}' to {self.relative_url}"


class PageLink(wagtail_models.Orderable):
    title = models.CharField(
        max_length=255,
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        related_name="+",
        on_delete=models.CASCADE,
        help_text="Title is changed to page title when using this page chooser, but can be altered afterwards.",
    )

    page = ParentalKey("Menu", related_name="page_links")

    panels = [
        FieldPanel("title"),
        PageChooserPanel("link_page"),
    ]

    def __str__(self):
        return f"{self.title} Link"


@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title", editable=True)

    panels = [
        FieldPanel("title"),
        InlinePanel("page_links", label="Page Link"),
    ]

    def __str__(self):
        return f"{self.title}"


class TableRow(blocks.StructBlock):
    column_1 = blocks.RichTextBlock(
        required=False,
        help_text=("Text for column 1"),
    )
    column_2 = blocks.RichTextBlock(
        required=False,
        help_text=("Text for column 2"),
    )
    social_media = SnippetChooserBlock(
        SocialMedia,
        required=False,
        help_text="Social media links will be shown with this row.",
    )

    class Column(models.IntegerChoices):
        COLUMN_1 = 1
        COLUMN_2 = 2

    social_media_column = blocks.ChoiceBlock(
        choices=Column.choices,
        required=False,
        help_text=("Under which column should social media links be placed?"),
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
        required=False,
        help_text=("Text for column 1"),
    )
    column_2 = blocks.RichTextBlock(
        required=False,
        help_text=("Text for column 2"),
    )
    column_3 = blocks.RichTextBlock(
        required=False,
        help_text=("Text for column 3"),
    )
    social_media = SnippetChooserBlock(
        SocialMedia,
        required=False,
        help_text="Social media links will be shown with this row.",
    )

    class Column(models.IntegerChoices):
        COLUMN_1 = 1
        COLUMN_2 = 2
        COLUMN_3 = 3

    social_media_column = blocks.ChoiceBlock(
        choices=Column.choices,
        required=False,
        help_text=("Under which column should social media links be placed?"),
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
        required=False,
        help_text=("Text for column 1"),
    )
    column_2 = blocks.RichTextBlock(
        required=False,
        help_text=("Text for column 2"),
    )
    column_3 = blocks.RichTextBlock(
        required=False,
        help_text=("Text for column 3"),
    )
    column_4 = blocks.RichTextBlock(
        required=False,
        help_text=("Text for column 4"),
    )
    social_media = SnippetChooserBlock(
        SocialMedia,
        required=False,
        help_text="Social media links will be shown with this row.",
    )

    class Column(models.IntegerChoices):
        COLUMN_1 = 1
        COLUMN_2 = 2
        COLUMN_3 = 3
        COLUMN_4 = 4

    social_media_column = blocks.ChoiceBlock(
        choices=Column.choices,
        required=False,
        help_text=("Under which column should social media links be placed?"),
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


class FiveColumnTableRow(blocks.StructBlock):
    column_1 = blocks.RichTextBlock(
        required=False,
        help_text=("Text for column 1"),
    )
    column_2 = blocks.RichTextBlock(
        required=False,
        help_text=("Text for column 2"),
    )
    column_3 = blocks.RichTextBlock(
        required=False,
        help_text=("Text for column 3"),
    )
    column_4 = blocks.RichTextBlock(
        required=False,
        help_text=("Text for column 4"),
    )
    column_5 = blocks.RichTextBlock(
        required=False,
        help_text=("Text for column 5"),
    )
    social_media = SnippetChooserBlock(
        SocialMedia,
        required=False,
        help_text="Social media links will be shown with this row.",
    )

    class Column(models.IntegerChoices):
        COLUMN_1 = 1
        COLUMN_2 = 2
        COLUMN_3 = 3
        COLUMN_4 = 4
        COLUMN_5 = 5

    social_media_column = blocks.ChoiceBlock(
        choices=Column.choices,
        required=False,
        help_text=("Under which column should social media links be placed?"),
    )

    class Meta:
        label = "Table row"
        form_classname = "five-column-table__row"


class FiveColumnTableRowStreamBlock(blocks.StreamBlock):
    rows = FiveColumnTableRow()


class FiveColumnBlock(blocks.StructBlock):
    has_grid_pattern = blocks.BooleanBlock(
        required=False, help_text="Does this table's styling have a grid pattern?"
    )
    is_first_row_header = blocks.BooleanBlock(
        required=False, help_text="Should the first row be displayed as a header?"
    )
    rows = FiveColumnTableRowStreamBlock()

    class Meta:
        template = "hip/text_or_table_stream.html"


class TextOrTableStreamBlock(blocks.StreamBlock):
    rich_text = blocks.RichTextBlock()
    two_column_table = TwoColumnBlock()
    three_column_table = ThreeColumnBlock()
    four_column_table = FourColumnBlock()
    five_column_table = FiveColumnBlock()


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
    button = SnippetChooserBlock(ButtonSnippet, required=False)


class StaticPage(HipBasePage):
    """A Page with only sections of static content."""

    subpage_types = ["hip.StaticPage", "hip.ListPage"]

    show_left_nav = models.BooleanField(
        default=True,
        blank=True,
        help_text="Should this page show a navigation of the site on the left side of the page?",
    )
    show_breadcrumb = models.BooleanField(
        default=False,
        blank=True,
        help_text="Should this page show a breadcrumb at the top of the page?",
    )
    show_back_button = models.BooleanField(
        default=False,
        blank=True,
        help_text="Should this page show a back button at the top of the page?",
    )
    show_right_nav = models.BooleanField(
        default=False,
        blank=True,
        help_text="Should this page show a navigation of its sections on the right side of the page?",
    )

    action_section = RichTextField(
        blank=True,
        help_text="This section will stand out to users, calling them to perform an action.",
    )
    body = StreamField(
        [
            ("section", StreamAndNavHeadingBlock()),
        ],
        use_json_field=True,
    )

    content_panels = HipBasePage.content_panels + [
        FieldPanel("show_left_nav"),
        FieldPanel("show_breadcrumb"),
        FieldPanel("show_back_button"),
        FieldPanel("show_right_nav"),
        FieldPanel("action_section"),
        FieldPanel("body"),
    ]
    search_fields = HipBasePage.search_fields + [
        index.SearchField("body"),
        index.SearchField("action_section"),
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
    subpage_types = ["hip.StaticPage", "hip.ListPage"]

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
        ],
        use_json_field=True,
    )

    content_panels = HipBasePage.content_panels + [
        FieldPanel("show_breadcrumb"),
        FieldPanel("show_right_nav"),
        FieldPanel("list_section"),
    ]
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
        use_json_field=True,
    )
    about = RichTextField(blank=True)
    contact_info = models.ForeignKey(
        "Contact", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    content_panels = HipBasePage.content_panels + [
        FieldPanel("short_description"),
        FieldPanel("contact_info"),
        FieldPanel("quick_links"),
        FieldPanel("about"),
    ]

    search_fields = HipBasePage.search_fields + [
        index.SearchField("quick_links"),
        index.SearchField("about"),
    ]

    def get_context(self, request):
        """Add recent_updates to context."""
        from apps.common.utils import get_all_pages_visible_to_request

        from .utils import get_most_recent_objects

        pages_visible_to_user = get_all_pages_visible_to_request(request)

        context = super().get_context(request)
        context["recent_updates"] = get_most_recent_objects(
            pages_qs=pages_visible_to_user, object_count=10
        )
        return context


class HIPDocumentQuerySet(DocumentQuerySet):
    def search(
        self,
        query,
        fields=None,
        operator=None,
        order_by_relevance=True,
        backend="default",
    ):
        """
        Implement our custom search method for HIPDocuments.

        Because partial matching is not supported for wagtail.contrib.postgres_search,
        we override this method to do a simple search for Documents with partial
        matching.
        """
        # Split the search terms based on spaces.
        search_terms = query.split(" ")
        # Loop through the search_terms, and add to q_terms. All of the search
        # terms have to be present for a HIPDocument to be matched.
        q_terms = models.Q()
        for term in search_terms:
            if term:
                q_terms &= models.Q(title__icontains=term)
        if q_terms != models.Q():
            return self.filter(q_terms)
        else:
            return self.none()


class HIPDocument(Document):
    """Define a custom document model, so that we can define a custom manager."""

    objects = HIPDocumentQuerySet.as_manager()

    @property
    def url(self, *args, **kwargs):
        if self.file:
            return reverse(
                "get_document",
                kwargs={"document_id": self.id, "document_name": self.filename},
            )
        return ""

from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.models import Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from apps.common.models import HipBasePage
from apps.disease_control.models import DiseaseAndConditionDetailPage


class PosterListPage(HipBasePage):
    # There can be only one PosterListPage
    max_count = 1
    parent_page_types = ["hip.HomePage"]
    subpage_types = ["posters.PosterDetailPage"]

    def get_context(self, request):
        """
        Add posters queryset and right_nav_headings to context.
        """
        context = super().get_context(request)

        # Get all live Posters, ordered by category, then by title
        posters = (
            PosterDetailPage.objects.child_of(self).order_by("category", "title").live()
        )
        context["posters"] = posters

        # Get list of categories that we have posters for, to create the right scroll
        # links and nav headings
        categories = [poster.category.name for poster in posters]
        # the following line removes duplicates but keeps things ordered (unlike sets)
        categories = list(dict.fromkeys(categories))
        context["right_nav_headings"] = categories

        return context


@register_snippet
class PosterCategory(models.Model):
    """
    Allow poster categories to be editable in the Wagtail admin.
    """

    name = models.CharField(max_length=255)

    panels = [FieldPanel("name")]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Poster Category"
        verbose_name_plural = "Poster Categories"


class PosterDetailPage(HipBasePage):
    parent_page_types = ["posters.PosterListPage"]
    subpage_types = []

    main_poster = models.ForeignKey(
        "wagtaildocs.Document", null=True, blank=False, on_delete=models.SET_NULL
    )

    thumbnail = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL
    )

    category = models.ForeignKey(
        PosterCategory, null=True, blank=True, on_delete=models.SET_NULL
    )

    disease = models.ForeignKey(
        DiseaseAndConditionDetailPage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posters",
    )

    content_panels = HipBasePage.content_panels + [
        DocumentChooserPanel("main_poster"),
        ImageChooserPanel("thumbnail"),
        InlinePanel("additional_versions", label="Additional versions of this poster"),
        FieldPanel("category"),
        FieldPanel("disease"),
    ]


class PosterDocumentVersion(Orderable):
    """
    Hold additional versions of a poster.

    So if the main poster is an english document, you might store a version in Spanish
    in this model, or versions of a different size.
    """

    page = ParentalKey(
        PosterDetailPage, on_delete=models.CASCADE, related_name="additional_versions"
    )
    document = models.ForeignKey(
        "wagtaildocs.Document", on_delete=models.CASCADE, related_name="+"
    )
    label = models.CharField(
        blank=False,
        max_length=30,
        help_text="A short label describing how this poster is different from the main poster. e.g. 'Spanish' or 'Vietnamese, 11 x 17'",
    )

    panels = [
        DocumentChooserPanel("document"),
        FieldPanel("label"),
    ]

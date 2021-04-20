from django.db import models
from django.utils.translation import gettext_lazy

from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from wagtail.admin.edit_handlers import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.core.models import Page
from wagtail.search import index


class IndexedTimeStampedModel(models.Model):
    created = AutoCreatedField("created", db_index=True)
    modified = AutoLastModifiedField("modified", db_index=True)

    class Meta:
        abstract = True


class HipBasePage(Page):
    """
    Base page that all HIP pages should inherit from so that they have the proper search fields
    and admin panels.
    """

    search_fields = Page.search_fields + [index.SearchField("search_description")]
    content_panels = Page.content_panels + [
        # show a HelpPanel explaining how to fill out search_description
        MultiFieldPanel(
            [
                HelpPanel(
                    content="The <strong>Search description</strong> field will be shown in search result listings and will also be included in the page's metadata for external search engines. It should be a short summary of the page's contents"
                ),
                FieldPanel("search_description"),
            ],
            heading="Search Description",
        )
    ]

    promote_panels = [
        # This MultiFieldPanel is copy-pasted from wagtail.admin.edit_handlers so we can override
        MultiFieldPanel(
            [
                FieldPanel("slug"),
                FieldPanel("seo_title"),
                # override Page's promote_panels to remove search_description (since we
                # include it in content_panels). Also, don't show "show_in_menus",
                # since we don't use that field in this project.
                # FieldPanel("show_in_menus"),
                # FieldPanel('search_description'),
            ],
            gettext_lazy("Common page configuration"),
        ),
    ]

    class Meta:
        abstract = True

    @property
    def is_closedpod_page(self):
        """
        Determine if this page is a Closed POD page.

        A page is a ClosedPOD page if it is either the ClosedPODHomePage, or a
        descendant of the ClosedPODHomePage.
        """
        if hasattr(self, "closedpodhomepage") or any(
            [
                hasattr(ancestor, "closedpodhomepage")
                for ancestor in self.get_ancestors()
            ]
        ):
            return True
        return False

    @property
    def is_pcwmsa_page(self):
        """
        Determine if this page is a PCW MSA page.

        A page is a PCW MSA page if it is either the PCWMSAHomePage, or a
        descendant of the PCWMSAHomePage.
        """
        if hasattr(self, "pcwmsahomepage") or any(
            [
                hasattr(ancestor.specific, "pcwmsahomepage")
                for ancestor in self.get_ancestors()
            ]
        ):
            return True
        return False

    @property
    def is_bigcities_page(self):
        """
        Determine if this page is a Big Cities page.

        A page is a Big Cities page if it is either the BigCitiesHomePage, or a
        descendant of the BigCitiesHomePage.
        """
        if hasattr(self, "bigcitieshomepage") or any(
            [
                hasattr(ancestor.specific, "bigcitieshomepage")
                for ancestor in self.get_ancestors()
            ]
        ):
            return True
        return False

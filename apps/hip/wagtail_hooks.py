from django.utils.html import escape, format_html

from sass_processor.processor import sass_processor
from wagtail import hooks
from wagtail.rich_text import LinkHandler


class ExternalLinkHandler(LinkHandler):
    identifier = "external"

    @classmethod
    def expand_db_attributes(cls, attrs):
        href = attrs["href"]
        return f'<a href="{escape(href)}" class="external-linktype">'


@hooks.register("insert_editor_css")
def editor_css():
    """Register the extra CSS styles to be used for the Wagtail editor."""
    return format_html(
        '<link rel="stylesheet" href="{}">',
        sass_processor("styles/wagtail_styles.scss"),
    )


@hooks.register("register_rich_text_features")
def register_external_link(features):
    features.register_link_type(ExternalLinkHandler)

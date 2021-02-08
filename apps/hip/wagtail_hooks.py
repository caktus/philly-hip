from django.utils.html import format_html

from sass_processor.processor import sass_processor
from wagtail.core import hooks


@hooks.register("insert_editor_css")
def editor_css():
    """Register the extra CSS styles to be used for the Wagtail editor."""
    return format_html(
        '<link rel="stylesheet" href="{}">',
        sass_processor("styles/wagtail_styles.scss"),
    )

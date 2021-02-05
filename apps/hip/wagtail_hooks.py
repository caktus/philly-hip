from django.templatetags.static import static
from django.utils.html import format_html

from wagtail.core import hooks


@hooks.register("insert_editor_css")
def editor_css():
    """Register the extra CSS styles to be used for the Wagtail editor."""
    return format_html(
        '<link rel="stylesheet" href="{}">', static("styles/wagtail_styles.css")
    )

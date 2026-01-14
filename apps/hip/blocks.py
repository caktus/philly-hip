from django.core import validators
from django.forms.fields import URLField

from wagtail import blocks


class HttpsUrlField(URLField):
    """
    A minimal adjustment to the URLField to ensure that
    only HTTPS URLs are accepted.
    """

    default_validators = [validators.URLValidator(schemes=["https"])]


class HttpsUrlBlock(blocks.FieldBlock):
    """
    A variation on the base Wagtail URLBlock, which simply wraps a URLField.
    """

    def __init__(
        self, required=True, help_text=None, max_length=None, min_length=None, **kwargs
    ):
        self.field = HttpsUrlField(
            required=required,
            help_text=help_text,
            max_length=max_length,
            min_length=min_length,
        )
        super().__init__(**kwargs)


class ExternalContentEmbedBlock(blocks.StructBlock):
    """
    Wagtail admin users can use this block to embed HTTP content using an iframe.
    They must provide a URL that will be the src for the iframe content from
    applications such as Tableau or Power BI.

    1. This block uses an iframe to display arbitrary content from another website.
    """

    heading = blocks.CharBlock()
    url = HttpsUrlBlock(
        help_text="This must be an HTTPs URL.",
        label="URL",
    )
    description = blocks.RichTextBlock(required=False)

    class Meta:
        template = "hip/code_embed.html"
        label = "Embed External Content"

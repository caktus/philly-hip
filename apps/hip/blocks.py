from wagtail import blocks


# We are creating new blocks in this file. In the future,
# let's migrate blocks from models.py to here.
class ExternalContentEmbedBlock(blocks.StructBlock):
    """
    Wagtail admin users can use this block to embed HTTP content using an iframe.
    They must provide an iframe from applications such as Tableau, Power BI, etc.
    """

    heading = blocks.CharBlock(required=False)
    code = blocks.RawHTMLBlock(
        required=True,
        help_text="Paste full iframe embed code here",
        label="Embed Code",
    )
    description = blocks.RichTextBlock(
        required=False, help_text="Details about the embedded content."
    )

    class Meta:
        template = "hip/code_embed.html"
        label = "Embed External Content"

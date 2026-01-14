from django.conf import settings
from django.core.exceptions import ValidationError

import pytest

from apps.hip.blocks import ExternalContentEmbedBlock, HttpsUrlBlock


def test_https_url_block_accepts_https():
    """Test that the block accepts a valid HTTPS URL."""
    block = HttpsUrlBlock()
    valid_url = "https://public.tableau.com/views/dashboard"
    assert block.clean(valid_url) == valid_url


def test_https_url_block_rejects_http():
    """Test that the block raises ValidationError for HTTP URLs."""
    block = HttpsUrlBlock()
    invalid_url = "http://insecure-site-url.com"

    with pytest.raises(ValidationError) as excinfo:
        block.clean(invalid_url)
    assert "Enter a valid URL" in str(excinfo.value)


@pytest.mark.django_db
def test_embed_block_get_context():
    """
    Verify that get_context injects 'iframe_width' and 'iframe_height'
    into the context dictionary.
    """
    block = ExternalContentEmbedBlock()
    value = block.to_python(
        {
            "heading": "Test Dashboard",
            "url": "https://public.tableau.com/views/test",
            "description": "<p>Text description</p>",
        }
    )

    context = block.get_context(value)
    assert context["iframe_width"] == settings.IFRAME_WIDTH
    assert context["iframe_height"] == settings.IFRAME_HEIGHT
    assert context["self"]["heading"] == value["heading"]


@pytest.mark.django_db
def test_embed_block_html_rendering():
    """
    Verify that the block renders the actual <iframe> tag with the
    style attributes derived from the context.
    """
    block = ExternalContentEmbedBlock()
    value = block.to_python(
        {
            "heading": "My Analytics",
            "url": "https://public.tableau.com/embed/123",
            "description": "Some insight here.",
        }
    )

    rendered_html = block.render(value)
    assert "<iframe" in rendered_html
    assert 'src="https://public.tableau.com/embed/123"' in rendered_html
    assert f"width: {settings.IFRAME_WIDTH}" in rendered_html
    assert f"height: {settings.IFRAME_HEIGHT}px" in rendered_html
    assert value["heading"] in rendered_html

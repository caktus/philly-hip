from django.core.exceptions import ValidationError

import pytest
from bs4 import BeautifulSoup
from wagtail.rich_text import RichText

from apps.hip.blocks import ExternalContentEmbedBlock


@pytest.mark.django_db
class TestExternalContentEmbedBlock:
    def render_block(self, value_overrides=None):
        block = ExternalContentEmbedBlock()
        block_value = {
            "heading": "My Analytics",
            "code": '<iframe src="https://public.tableau.com/embed/123" width="800" title="Tableau Dashboard"></iframe>',
            "description": "<p>Some insight here.</p>",
        }
        if value_overrides:
            block_value.update(value_overrides)

        value = block.to_python(block_value)
        return block.render(value)

    def test_embed_block_required_fields(self):
        """
        Test that the 'code' field is required, but optional fields aren't.
        """
        block = ExternalContentEmbedBlock()
        invalid_data = {
            "heading": "Dashboard",
            "description": RichText("Optional text"),
            "code": "",
        }

        with pytest.raises(ValidationError) as excinfo:
            block.clean(invalid_data)

        assert "code" in excinfo.value.block_errors
        assert "This field is required" in str(excinfo.value.block_errors["code"])

    def test_embed_block_optional_fields(self):
        """
        Test that the block validates successfully with heading & description missing.
        """
        block = ExternalContentEmbedBlock()

        sample_iframe = '<iframe src="https://example.com"></iframe>'

        valid_data = {
            "heading": "",
            "description": RichText(""),
            "code": sample_iframe,
        }

        try:
            cleaned_value = block.clean(valid_data)
            assert cleaned_value["code"] == sample_iframe
        except ValidationError:
            pytest.fail("Block failed validation with valid required fields.")

    def test_embed_block_html_rendering(self):
        """
        Verify that the block renders raw HTML code with responsive wrapper markup.
        """
        rendered_html = self.render_block()
        soup = BeautifulSoup(rendered_html, "html.parser")

        wrapper = soup.select_one(".code-embed-hip.js-code-embed-hip")
        assert wrapper is not None

        scroll_area = wrapper.select_one(
            ".code-embed-scroll-hip.is-flex.is-justify-content-center.js-code-embed-scroll-hip"
        )
        assert scroll_area is not None

        content = scroll_area.select_one(".code-embed-content-hip")
        assert content is not None

        iframe = content.find("iframe")
        assert iframe is not None
        assert iframe["src"] == "https://public.tableau.com/embed/123"
        assert iframe["width"] == "800"
        assert iframe["title"] == "Tableau Dashboard"

        hint = scroll_area.select_one(
            ".code-embed-pinch-hint-hip.js-code-embed-hint-hip"
        )
        assert hint is not None
        assert hint["aria-hidden"] == "true"
        assert hint.get_text(" ", strip=True) == "Pinch to zoom. Swipe to scroll."

        heading = soup.find("h2")
        assert heading is not None
        assert heading.get_text(strip=True) == "My Analytics"

        description = soup.select_one(".has-text-centered.mt-4")
        assert description is not None
        assert description.get_text(" ", strip=True) == "Some insight here."

    def test_embed_block_preserves_complex_tableau_embed_markup(self):
        """
        Verify that multi-tag embed code is preserved inside the content wrapper.
        """
        embed_markup = """\
<div class="tableauPlaceholder" id="viz1680000000000"></div>
<script type="text/javascript">var foo = "bar";</script>
<iframe src="https://public.tableau.com/views/dashboard" width="1200"></iframe>
"""

        rendered_html = self.render_block({"code": embed_markup})
        soup = BeautifulSoup(rendered_html, "html.parser")
        content = soup.select_one(".code-embed-content-hip")

        assert content is not None
        assert content.select_one(".tableauPlaceholder#viz1680000000000") is not None

        script_tag = content.find("script")
        assert script_tag is not None
        assert script_tag["type"] == "text/javascript"
        assert 'var foo = "bar";' in script_tag.string

        iframe = content.find("iframe")
        assert iframe is not None
        assert iframe["src"] == "https://public.tableau.com/views/dashboard"
        assert iframe["width"] == "1200"

    def test_embed_block_omits_heading_markup_when_heading_is_blank(self):
        """
        Verify that no heading element is rendered when heading is omitted.
        """
        rendered_html = self.render_block({"heading": ""})
        soup = BeautifulSoup(rendered_html, "html.parser")

        assert soup.find("h2") is None
        assert soup.select_one(".code-embed-hip") is not None

    def test_embed_block_omits_description_container_when_description_is_blank(self):
        """
        Verify that no description container is rendered when description is omitted.
        """
        rendered_html = self.render_block({"description": ""})
        soup = BeautifulSoup(rendered_html, "html.parser")

        assert soup.select_one(".has-text-centered.mt-4") is None
        assert soup.select_one(".code-embed-pinch-hint-hip") is not None

    def test_embed_block_renders_single_mobile_hint_per_embed(self):
        """
        Verify that each embed block renders a single mobile hint element.
        """
        rendered_html = self.render_block()
        soup = BeautifulSoup(rendered_html, "html.parser")

        hints = soup.select(".code-embed-pinch-hint-hip.js-code-embed-hint-hip")

        assert len(hints) == 1
        assert hints[0].get_text(" ", strip=True) == "Pinch to zoom. Swipe to scroll."

    def test_embed_block_unicode_support(self):
        """
        Test that the block handles and renders Unicode characters (emojis, accents) correctly.
        """
        block = ExternalContentEmbedBlock()
        heading_text = "Dàshbøard 📊"
        code_text = '<iframe src="https://test.com" title="Vidéø"></iframe>'
        desc_text = "Déjà vu! 🧐"
        value = block.to_python(
            {"heading": heading_text, "code": code_text, "description": desc_text}
        )
        rendered_html = block.render(value)

        assert heading_text in rendered_html
        assert code_text in rendered_html
        assert desc_text in rendered_html

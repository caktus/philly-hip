from django.core.exceptions import ValidationError

import pytest
from wagtail.rich_text import RichText

from apps.hip.blocks import ExternalContentEmbedBlock


@pytest.mark.django_db
class TestExternalContentEmbedBlock:
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
        Verify that the block renders the raw HTML code inside the flex container.
        """
        block = ExternalContentEmbedBlock()
        sample_code = (
            '<iframe src="https://public.tableau.com/embed/123" width="800"></iframe>'
        )
        value = block.to_python(
            {
                "heading": "My Analytics",
                "code": sample_code,
                "description": "Some insight here.",
            }
        )
        rendered_html = block.render(value)

        assert "is-flex is-justify-content-center" in rendered_html
        assert sample_code in rendered_html
        assert "My Analytics" in rendered_html

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

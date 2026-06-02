from wagtail import blocks


class DescriptionBlock(blocks.RichTextBlock):
    """Block for the disease/condition description."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    class Meta:
        label = "Description"
        help_text = "Enter a short description which will be shown on the page listing diseases and conditions."


class AtAGlanceBlock(blocks.RichTextBlock):
    """Block for at a glance information."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    class Meta:
        label = "At a Glance"


class CurrentRecommendationsBlock(blocks.RichTextBlock):
    """Block for current recommendations."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    class Meta:
        label = "Current Recommendations"


class SurveillanceBlock(blocks.RichTextBlock):
    """Block for surveillance information."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    class Meta:
        label = "Surveillance"


class VaccineInfoBlock(blocks.RichTextBlock):
    """Block for vaccine information."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    class Meta:
        label = "Vaccine Info"


class DiagnosisInfoBlock(blocks.RichTextBlock):
    """Block for diagnosis and management information."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    class Meta:
        label = "Diagnosis & Management"


class ProviderResourcesBlock(blocks.RichTextBlock):
    """Block for healthcare provider resources."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    class Meta:
        label = "Provider Resources"
        help_text = "List resources that will be useful for healthcare providers. Resources for patients and community will be pulled automatically by including any documents that are tagged with the title of this disease/condition."

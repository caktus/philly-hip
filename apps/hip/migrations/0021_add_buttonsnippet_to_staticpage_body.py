# Generated by Django 3.1.8 on 2021-06-11 18:00

from django.db import migrations

import wagtail.core.blocks
import wagtail.core.fields
import wagtail.snippets.blocks

import apps.hip.models


class Migration(migrations.Migration):

    dependencies = [
        ("hip", "0020_buttonsnippet"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staticpage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "section",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "nav_heading",
                                    wagtail.core.blocks.CharBlock(
                                        help_text="The heading that should appear for this section in the scrolling navigation on the side of the page.",
                                        max_length=80,
                                        required=False,
                                    ),
                                ),
                                (
                                    "is_card",
                                    wagtail.core.blocks.BooleanBlock(
                                        help_text="Is this content block a card?",
                                        required=False,
                                    ),
                                ),
                                (
                                    "body",
                                    wagtail.core.blocks.StreamBlock(
                                        [
                                            (
                                                "rich_text",
                                                wagtail.core.blocks.RichTextBlock(),
                                            ),
                                            (
                                                "two_column_table",
                                                wagtail.core.blocks.StructBlock(
                                                    [
                                                        (
                                                            "has_grid_pattern",
                                                            wagtail.core.blocks.BooleanBlock(
                                                                help_text="Does this table's styling have a grid pattern?",
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "is_first_row_header",
                                                            wagtail.core.blocks.BooleanBlock(
                                                                help_text="Should the first row be displayed as a header?",
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "rows",
                                                            wagtail.core.blocks.StreamBlock(
                                                                [
                                                                    (
                                                                        "rows",
                                                                        wagtail.core.blocks.StructBlock(
                                                                            [
                                                                                (
                                                                                    "column_1",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 1",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "column_2",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 2",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "social_media",
                                                                                    wagtail.snippets.blocks.SnippetChooserBlock(
                                                                                        apps.hip.models.SocialMedia,
                                                                                        help_text="Social media links will be shown with this row.",
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "social_media_column",
                                                                                    wagtail.core.blocks.ChoiceBlock(
                                                                                        choices=[
                                                                                            (
                                                                                                1,
                                                                                                "Column 1",
                                                                                            ),
                                                                                            (
                                                                                                2,
                                                                                                "Column 2",
                                                                                            ),
                                                                                        ],
                                                                                        help_text="Under which column should social media links be placed?",
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                            ]
                                                                        ),
                                                                    )
                                                                ]
                                                            ),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                            (
                                                "three_column_table",
                                                wagtail.core.blocks.StructBlock(
                                                    [
                                                        (
                                                            "has_grid_pattern",
                                                            wagtail.core.blocks.BooleanBlock(
                                                                help_text="Does this table's styling have a grid pattern?",
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "is_first_row_header",
                                                            wagtail.core.blocks.BooleanBlock(
                                                                help_text="Should the first row be displayed as a header?",
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "rows",
                                                            wagtail.core.blocks.StreamBlock(
                                                                [
                                                                    (
                                                                        "rows",
                                                                        wagtail.core.blocks.StructBlock(
                                                                            [
                                                                                (
                                                                                    "column_1",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 1",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "column_2",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 2",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "column_3",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 3",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "social_media",
                                                                                    wagtail.snippets.blocks.SnippetChooserBlock(
                                                                                        apps.hip.models.SocialMedia,
                                                                                        help_text="Social media links will be shown with this row.",
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "social_media_column",
                                                                                    wagtail.core.blocks.ChoiceBlock(
                                                                                        choices=[
                                                                                            (
                                                                                                1,
                                                                                                "Column 1",
                                                                                            ),
                                                                                            (
                                                                                                2,
                                                                                                "Column 2",
                                                                                            ),
                                                                                            (
                                                                                                3,
                                                                                                "Column 3",
                                                                                            ),
                                                                                        ],
                                                                                        help_text="Under which column should social media links be placed?",
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                            ]
                                                                        ),
                                                                    )
                                                                ]
                                                            ),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                            (
                                                "four_column_table",
                                                wagtail.core.blocks.StructBlock(
                                                    [
                                                        (
                                                            "has_grid_pattern",
                                                            wagtail.core.blocks.BooleanBlock(
                                                                help_text="Does this table's styling have a grid pattern?",
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "is_first_row_header",
                                                            wagtail.core.blocks.BooleanBlock(
                                                                help_text="Should the first row be displayed as a header?",
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "rows",
                                                            wagtail.core.blocks.StreamBlock(
                                                                [
                                                                    (
                                                                        "rows",
                                                                        wagtail.core.blocks.StructBlock(
                                                                            [
                                                                                (
                                                                                    "column_1",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 1",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "column_2",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 2",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "column_3",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 3",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "column_4",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 4",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "social_media",
                                                                                    wagtail.snippets.blocks.SnippetChooserBlock(
                                                                                        apps.hip.models.SocialMedia,
                                                                                        help_text="Social media links will be shown with this row.",
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "social_media_column",
                                                                                    wagtail.core.blocks.ChoiceBlock(
                                                                                        choices=[
                                                                                            (
                                                                                                1,
                                                                                                "Column 1",
                                                                                            ),
                                                                                            (
                                                                                                2,
                                                                                                "Column 2",
                                                                                            ),
                                                                                            (
                                                                                                3,
                                                                                                "Column 3",
                                                                                            ),
                                                                                            (
                                                                                                4,
                                                                                                "Column 4",
                                                                                            ),
                                                                                        ],
                                                                                        help_text="Under which column should social media links be placed?",
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                            ]
                                                                        ),
                                                                    )
                                                                ]
                                                            ),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                            (
                                                "five_column_table",
                                                wagtail.core.blocks.StructBlock(
                                                    [
                                                        (
                                                            "has_grid_pattern",
                                                            wagtail.core.blocks.BooleanBlock(
                                                                help_text="Does this table's styling have a grid pattern?",
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "is_first_row_header",
                                                            wagtail.core.blocks.BooleanBlock(
                                                                help_text="Should the first row be displayed as a header?",
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "rows",
                                                            wagtail.core.blocks.StreamBlock(
                                                                [
                                                                    (
                                                                        "rows",
                                                                        wagtail.core.blocks.StructBlock(
                                                                            [
                                                                                (
                                                                                    "column_1",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 1",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "column_2",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 2",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "column_3",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 3",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "column_4",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 4",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "column_5",
                                                                                    wagtail.core.blocks.RichTextBlock(
                                                                                        help_text="Text for column 5",
                                                                                        max_length=255,
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "social_media",
                                                                                    wagtail.snippets.blocks.SnippetChooserBlock(
                                                                                        apps.hip.models.SocialMedia,
                                                                                        help_text="Social media links will be shown with this row.",
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                                (
                                                                                    "social_media_column",
                                                                                    wagtail.core.blocks.ChoiceBlock(
                                                                                        choices=[
                                                                                            (
                                                                                                1,
                                                                                                "Column 1",
                                                                                            ),
                                                                                            (
                                                                                                2,
                                                                                                "Column 2",
                                                                                            ),
                                                                                            (
                                                                                                3,
                                                                                                "Column 3",
                                                                                            ),
                                                                                            (
                                                                                                4,
                                                                                                "Column 4",
                                                                                            ),
                                                                                            (
                                                                                                5,
                                                                                                "Column 5",
                                                                                            ),
                                                                                        ],
                                                                                        help_text="Under which column should social media links be placed?",
                                                                                        required=False,
                                                                                    ),
                                                                                ),
                                                                            ]
                                                                        ),
                                                                    )
                                                                ]
                                                            ),
                                                        ),
                                                    ]
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                                (
                                    "contact_info",
                                    wagtail.snippets.blocks.SnippetChooserBlock(
                                        apps.hip.models.Contact, required=False
                                    ),
                                ),
                                (
                                    "button",
                                    wagtail.snippets.blocks.SnippetChooserBlock(
                                        apps.hip.models.ButtonSnippet, required=False
                                    ),
                                ),
                            ]
                        ),
                    )
                ]
            ),
        ),
    ]

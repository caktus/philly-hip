# Generated by Django 3.1.6 on 2021-03-29 12:11

from django.db import migrations

import wagtail.core.blocks
import wagtail.core.fields
import wagtail.snippets.blocks

import apps.hip.models


class Migration(migrations.Migration):

    dependencies = [
        ("hip", "0008_homepage_short_description"),
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
                            ]
                        ),
                    )
                ]
            ),
        ),
    ]

# Generated by Django 3.1.5 on 2021-02-03 13:54

import django.db.models.deletion
from django.db import migrations, models

import wagtail.contrib.table_block.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0059_apply_collection_ordering"),
    ]

    operations = [
        migrations.CreateModel(
            name="StaticPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "body",
                    wagtail.core.fields.StreamField(
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
                                            "body",
                                            wagtail.core.blocks.StreamBlock(
                                                [
                                                    (
                                                        "rich_text",
                                                        wagtail.core.blocks.RichTextBlock(),
                                                    ),
                                                    (
                                                        "table",
                                                        wagtail.contrib.table_block.blocks.TableBlock(),
                                                    ),
                                                ]
                                            ),
                                        ),
                                    ]
                                ),
                            )
                        ]
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]

# Generated by Django 3.1.6 on 2021-03-26 15:06

from django.db import migrations

import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="datareportlistpage",
            name="external_reports",
            field=wagtail.fields.StreamField(
                [
                    (
                        "external_reports",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.blocks.CharBlock(
                                        help_text="The title of the external report.",
                                        max_length=255,
                                        required=True,
                                    ),
                                ),
                                (
                                    "url",
                                    wagtail.blocks.URLBlock(
                                        help_text="The URL to the external report.",
                                        required=True,
                                    ),
                                ),
                                (
                                    "update_frequency",
                                    wagtail.blocks.CharBlock(
                                        help_text="How often this external is udpated (Annually, Quarterly, etc.).",
                                        max_length=255,
                                        required=True,
                                    ),
                                ),
                                (
                                    "last_updated",
                                    wagtail.blocks.DateBlock(required=True),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
            ),
        ),
    ]

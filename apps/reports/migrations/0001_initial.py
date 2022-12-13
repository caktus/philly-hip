# Generated by Django 3.1.6 on 2021-03-25 18:24

import django.db.models.deletion
from django.db import migrations, models

import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0060_fix_workflow_unique_constraint"),
        ("hip", "0008_homepage_short_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="DataReportListPage",
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
                ("description", wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="DataReportDetailPage",
            fields=[
                (
                    "staticpage_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="hip.staticpage",
                    ),
                ),
                ("update_frequency", models.CharField(blank=True, max_length=80)),
                (
                    "associated_disease",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="data_report_detail_pages",
                        to="wagtailcore.page",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("hip.staticpage",),
        ),
    ]

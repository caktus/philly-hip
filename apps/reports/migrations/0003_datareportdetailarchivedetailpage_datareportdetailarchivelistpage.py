# Generated by Django 3.1.6 on 2021-03-30 00:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hip", "0009_add_staticpage_four_column_table"),
        ("wagtailcore", "0060_fix_workflow_unique_constraint"),
        ("reports", "0002_datareportlistpage_external_reports"),
    ]

    operations = [
        migrations.CreateModel(
            name="DataReportDetailArchiveDetailPage",
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
                ("year", models.PositiveSmallIntegerField()),
            ],
            options={
                "abstract": False,
            },
            bases=("hip.staticpage",),
        ),
        migrations.CreateModel(
            name="DataReportDetailArchiveListPage",
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
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]

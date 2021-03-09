# Generated by Django 3.1.6 on 2021-03-05 20:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0060_fix_workflow_unique_constraint"),
        ("disease_control", "0005_add_disease_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmergentHealthTopicsPage",
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
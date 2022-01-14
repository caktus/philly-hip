# Generated by Django 3.2.10 on 2022-01-14 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hip", "0022_create_button_snippets_for_forms"),
        ("health_alerts", "0007_auto_20210319_1659"),
    ]

    operations = [
        migrations.AlterField(
            model_name="healthalertdetailpage",
            name="alert_file",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="hip.hipdocument",
            ),
        ),
    ]

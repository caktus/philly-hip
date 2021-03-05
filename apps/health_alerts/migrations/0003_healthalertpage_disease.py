# Generated by Django 3.1.6 on 2021-03-05 19:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disease_control', '0005_auto_20210305_1448'),
        ('health_alerts', '0002_healthalertpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthalertpage',
            name='disease',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='health_alerts', to='disease_control.diseasepage'),
        ),
    ]

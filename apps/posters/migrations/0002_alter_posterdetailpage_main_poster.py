# Generated by Django 3.2.5 on 2022-01-18 18:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hip', '0022_create_button_snippets_for_forms'),
        ('posters', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posterdetailpage',
            name='main_poster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hip.hipdocument'),
        ),
    ]
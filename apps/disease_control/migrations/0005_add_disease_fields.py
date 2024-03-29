# Generated by Django 3.1.6 on 2021-03-06 13:32

from django.db import migrations

import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('disease_control', '0004_diseasepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='diseasepage',
            name='at_a_glance',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='diseasepage',
            name='current_recommendations',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='diseasepage',
            name='diagnosis_info',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='diseasepage',
            name='provider_resources',
            field=wagtail.fields.RichTextField(blank=True, help_text='List resources that will be useful for healthcare providers. Resources for patients and community will be pulled automatically by including any documents that are tagged with the title of this disease/condition.'),
        ),
        migrations.AddField(
            model_name='diseasepage',
            name='surveillance',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='diseasepage',
            name='vaccine_info',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='diseasepage',
            name='description',
            field=wagtail.fields.RichTextField(blank=True, help_text='Enter a short description which will be shown on the page listing diseases and conditions.'),
        ),
    ]

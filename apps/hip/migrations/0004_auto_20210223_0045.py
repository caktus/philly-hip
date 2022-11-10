# Generated by Django 3.1.5 on 2021-02-23 00:45

import django.utils.timezone
from django.db import migrations, models

import model_utils.fields
import phonenumber_field.modelfields
import wagtail.blocks
import wagtail.fields
import wagtail.snippets.blocks

import apps.hip.models


class Migration(migrations.Migration):

    dependencies = [
        ('hip', '0003_quicklinks_internal_or_external'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('business_hours_call_number', phonenumber_field.modelfields.PhoneNumberField(help_text='Business Hours Call Number', max_length=128, region=None)),
                ('business_hours_fax_number', phonenumber_field.modelfields.PhoneNumberField(help_text='Business Hours Fax Number', max_length=128, region=None)),
                ('after_hours_call_number', phonenumber_field.modelfields.PhoneNumberField(help_text='After Hours Call Number', max_length=128, region=None)),
            ],
            options={
                'verbose_name': 'Contact Us',
                'verbose_name_plural': 'Contact Us',
            },
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='body',
            field=wagtail.fields.StreamField([('section', wagtail.blocks.StructBlock([('nav_heading', wagtail.blocks.CharBlock(help_text='The heading that should appear for this section in the scrolling navigation on the side of the page.', max_length=80, required=False)), ('is_card', wagtail.blocks.BooleanBlock(help_text='Is this content block a card?', required=False)), ('body', wagtail.blocks.StreamBlock([('rich_text', wagtail.blocks.RichTextBlock()), ('two_column_table', wagtail.blocks.StructBlock([('has_grid_pattern', wagtail.blocks.BooleanBlock(help_text="Does this table's styling have a grid pattern?", required=False)), ('is_first_row_header', wagtail.blocks.BooleanBlock(help_text='Should the first row be displayed as a header?', required=False)), ('rows', wagtail.blocks.StreamBlock([('rows', wagtail.blocks.StructBlock([('column_1', wagtail.blocks.RichTextBlock(help_text='Text for column 1', max_length=255, required=False)), ('column_2', wagtail.blocks.RichTextBlock(help_text='Text for column 2', max_length=255, required=False))]))]))]))])), ('contact_info', wagtail.snippets.blocks.SnippetChooserBlock(apps.hip.models.Contact, required=False))]))]),
        ),
    ]

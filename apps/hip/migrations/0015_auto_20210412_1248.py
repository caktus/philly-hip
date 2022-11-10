# Generated by Django 3.1.6 on 2021-04-12 16:48

import django.utils.timezone
from django.db import migrations, models

import model_utils.fields
import wagtail.blocks
import wagtail.fields
import wagtail.snippets.blocks

import apps.hip.models


class Migration(migrations.Migration):

    dependencies = [
        ('hip', '0014_staticpage_fields_for_nav_backbutton_and_breadcrumb'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('org_name', models.CharField(max_length=255, verbose_name='Organization Name')),
                ('twitter', models.URLField(blank=True, max_length=255)),
                ('facebook', models.URLField(blank=True, max_length=255)),
                ('instagram', models.URLField(blank=True, max_length=255)),
                ('youtube', models.URLField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Social Media',
                'verbose_name_plural': 'Social Media',
            },
        ),
        migrations.AlterField(
            model_name='staticpage',
            name='body',
            field=wagtail.fields.StreamField([('section', wagtail.blocks.StructBlock([('nav_heading', wagtail.blocks.CharBlock(help_text='The heading that should appear for this section in the scrolling navigation on the side of the page.', max_length=80, required=False)), ('is_card', wagtail.blocks.BooleanBlock(help_text='Is this content block a card?', required=False)), ('body', wagtail.blocks.StreamBlock([('rich_text', wagtail.blocks.RichTextBlock()), ('two_column_table', wagtail.blocks.StructBlock([('has_grid_pattern', wagtail.blocks.BooleanBlock(help_text="Does this table's styling have a grid pattern?", required=False)), ('is_first_row_header', wagtail.blocks.BooleanBlock(help_text='Should the first row be displayed as a header?', required=False)), ('rows', wagtail.blocks.StreamBlock([('rows', wagtail.blocks.StructBlock([('column_1', wagtail.blocks.RichTextBlock(help_text='Text for column 1', max_length=255, required=False)), ('column_2', wagtail.blocks.RichTextBlock(help_text='Text for column 2', max_length=255, required=False)), ('social_media', wagtail.snippets.blocks.SnippetChooserBlock(apps.hip.models.SocialMedia, help_text='Social media links will be shown with this row.', required=False))]))]))])), ('three_column_table', wagtail.blocks.StructBlock([('has_grid_pattern', wagtail.blocks.BooleanBlock(help_text="Does this table's styling have a grid pattern?", required=False)), ('is_first_row_header', wagtail.blocks.BooleanBlock(help_text='Should the first row be displayed as a header?', required=False)), ('rows', wagtail.blocks.StreamBlock([('rows', wagtail.blocks.StructBlock([('column_1', wagtail.blocks.RichTextBlock(help_text='Text for column 1', max_length=255, required=False)), ('column_2', wagtail.blocks.RichTextBlock(help_text='Text for column 2', max_length=255, required=False)), ('column_3', wagtail.blocks.RichTextBlock(help_text='Text for column 3', max_length=255, required=False)), ('social_media', wagtail.snippets.blocks.SnippetChooserBlock(apps.hip.models.SocialMedia, help_text='Social media links will be shown with this row.', required=False))]))]))])), ('four_column_table', wagtail.blocks.StructBlock([('has_grid_pattern', wagtail.blocks.BooleanBlock(help_text="Does this table's styling have a grid pattern?", required=False)), ('is_first_row_header', wagtail.blocks.BooleanBlock(help_text='Should the first row be displayed as a header?', required=False)), ('rows', wagtail.blocks.StreamBlock([('rows', wagtail.blocks.StructBlock([('column_1', wagtail.blocks.RichTextBlock(help_text='Text for column 1', max_length=255, required=False)), ('column_2', wagtail.blocks.RichTextBlock(help_text='Text for column 2', max_length=255, required=False)), ('column_3', wagtail.blocks.RichTextBlock(help_text='Text for column 3', max_length=255, required=False)), ('column_4', wagtail.blocks.RichTextBlock(help_text='Text for column 4', max_length=255, required=False)), ('social_media', wagtail.snippets.blocks.SnippetChooserBlock(apps.hip.models.SocialMedia, help_text='Social media links will be shown with this row.', required=False))]))]))])), ('five_column_table', wagtail.blocks.StructBlock([('has_grid_pattern', wagtail.blocks.BooleanBlock(help_text="Does this table's styling have a grid pattern?", required=False)), ('is_first_row_header', wagtail.blocks.BooleanBlock(help_text='Should the first row be displayed as a header?', required=False)), ('rows', wagtail.blocks.StreamBlock([('rows', wagtail.blocks.StructBlock([('column_1', wagtail.blocks.RichTextBlock(help_text='Text for column 1', max_length=255, required=False)), ('column_2', wagtail.blocks.RichTextBlock(help_text='Text for column 2', max_length=255, required=False)), ('column_3', wagtail.blocks.RichTextBlock(help_text='Text for column 3', max_length=255, required=False)), ('column_4', wagtail.blocks.RichTextBlock(help_text='Text for column 4', max_length=255, required=False)), ('column_5', wagtail.blocks.RichTextBlock(help_text='Text for column 5', max_length=255, required=False)), ('social_media', wagtail.snippets.blocks.SnippetChooserBlock(apps.hip.models.SocialMedia, help_text='Social media links will be shown with this row.', required=False))]))]))]))])), ('contact_info', wagtail.snippets.blocks.SnippetChooserBlock(apps.hip.models.Contact, required=False))]))]),
        ),
    ]

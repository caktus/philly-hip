# Generated by Django 3.2.16 on 2022-10-25 14:52

from django.db import migrations

import wagtail.blocks
import wagtail.fields
import wagtail.snippets.blocks

import apps.hip.models


class Migration(migrations.Migration):

    dependencies = [
        ('disease_control', '0015_add_buttonsnippet_to_diseasecontrolchildstaticpage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diseasecontrolchildlistpage',
            name='list_section',
            field=wagtail.fields.StreamField([('list_section', wagtail.blocks.StructBlock([('header', wagtail.blocks.CharBlock(help_text='The heading for this section of rows (maximum of 80 characters).', max_length=80, required=False)), ('show_header_in_right_nav', wagtail.blocks.BooleanBlock(default=True, help_text='Should this header be shown in the navigation on the right side of the page?', required=False)), ('rows', wagtail.blocks.StreamBlock([('rows', wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock(help_text='An internal page', required=True)), ('description', wagtail.blocks.RichTextBlock(help_text='Description for this row', required=False))]))]))]))], use_json_field=True),
        ),
        migrations.AlterField(
            model_name='diseasecontrolchildstaticpage',
            name='body',
            field=wagtail.fields.StreamField([('section', wagtail.blocks.StructBlock([('nav_heading', wagtail.blocks.CharBlock(help_text='The heading that should appear for this section in the scrolling navigation on the side of the page.', max_length=80, required=False)), ('is_card', wagtail.blocks.BooleanBlock(help_text='Is this content block a card?', required=False)), ('body', wagtail.blocks.StreamBlock([('rich_text', wagtail.blocks.RichTextBlock()), ('two_column_table', wagtail.blocks.StructBlock([('has_grid_pattern', wagtail.blocks.BooleanBlock(help_text="Does this table's styling have a grid pattern?", required=False)), ('is_first_row_header', wagtail.blocks.BooleanBlock(help_text='Should the first row be displayed as a header?', required=False)), ('rows', wagtail.blocks.StreamBlock([('rows', wagtail.blocks.StructBlock([('column_1', wagtail.blocks.RichTextBlock(help_text='Text for column 1', max_length=255, required=False)), ('column_2', wagtail.blocks.RichTextBlock(help_text='Text for column 2', max_length=255, required=False)), ('social_media', wagtail.snippets.blocks.SnippetChooserBlock(apps.hip.models.SocialMedia, help_text='Social media links will be shown with this row.', required=False)), ('social_media_column', wagtail.blocks.ChoiceBlock(choices=[(1, 'Column 1'), (2, 'Column 2')], help_text='Under which column should social media links be placed?', required=False))]))]))])), ('three_column_table', wagtail.blocks.StructBlock([('has_grid_pattern', wagtail.blocks.BooleanBlock(help_text="Does this table's styling have a grid pattern?", required=False)), ('is_first_row_header', wagtail.blocks.BooleanBlock(help_text='Should the first row be displayed as a header?', required=False)), ('rows', wagtail.blocks.StreamBlock([('rows', wagtail.blocks.StructBlock([('column_1', wagtail.blocks.RichTextBlock(help_text='Text for column 1', max_length=255, required=False)), ('column_2', wagtail.blocks.RichTextBlock(help_text='Text for column 2', max_length=255, required=False)), ('column_3', wagtail.blocks.RichTextBlock(help_text='Text for column 3', max_length=255, required=False)), ('social_media', wagtail.snippets.blocks.SnippetChooserBlock(apps.hip.models.SocialMedia, help_text='Social media links will be shown with this row.', required=False)), ('social_media_column', wagtail.blocks.ChoiceBlock(choices=[(1, 'Column 1'), (2, 'Column 2'), (3, 'Column 3')], help_text='Under which column should social media links be placed?', required=False))]))]))])), ('four_column_table', wagtail.blocks.StructBlock([('has_grid_pattern', wagtail.blocks.BooleanBlock(help_text="Does this table's styling have a grid pattern?", required=False)), ('is_first_row_header', wagtail.blocks.BooleanBlock(help_text='Should the first row be displayed as a header?', required=False)), ('rows', wagtail.blocks.StreamBlock([('rows', wagtail.blocks.StructBlock([('column_1', wagtail.blocks.RichTextBlock(help_text='Text for column 1', max_length=255, required=False)), ('column_2', wagtail.blocks.RichTextBlock(help_text='Text for column 2', max_length=255, required=False)), ('column_3', wagtail.blocks.RichTextBlock(help_text='Text for column 3', max_length=255, required=False)), ('column_4', wagtail.blocks.RichTextBlock(help_text='Text for column 4', max_length=255, required=False)), ('social_media', wagtail.snippets.blocks.SnippetChooserBlock(apps.hip.models.SocialMedia, help_text='Social media links will be shown with this row.', required=False)), ('social_media_column', wagtail.blocks.ChoiceBlock(choices=[(1, 'Column 1'), (2, 'Column 2'), (3, 'Column 3'), (4, 'Column 4')], help_text='Under which column should social media links be placed?', required=False))]))]))])), ('five_column_table', wagtail.blocks.StructBlock([('has_grid_pattern', wagtail.blocks.BooleanBlock(help_text="Does this table's styling have a grid pattern?", required=False)), ('is_first_row_header', wagtail.blocks.BooleanBlock(help_text='Should the first row be displayed as a header?', required=False)), ('rows', wagtail.blocks.StreamBlock([('rows', wagtail.blocks.StructBlock([('column_1', wagtail.blocks.RichTextBlock(help_text='Text for column 1', max_length=255, required=False)), ('column_2', wagtail.blocks.RichTextBlock(help_text='Text for column 2', max_length=255, required=False)), ('column_3', wagtail.blocks.RichTextBlock(help_text='Text for column 3', max_length=255, required=False)), ('column_4', wagtail.blocks.RichTextBlock(help_text='Text for column 4', max_length=255, required=False)), ('column_5', wagtail.blocks.RichTextBlock(help_text='Text for column 5', max_length=255, required=False)), ('social_media', wagtail.snippets.blocks.SnippetChooserBlock(apps.hip.models.SocialMedia, help_text='Social media links will be shown with this row.', required=False)), ('social_media_column', wagtail.blocks.ChoiceBlock(choices=[(1, 'Column 1'), (2, 'Column 2'), (3, 'Column 3'), (4, 'Column 4'), (5, 'Column 5')], help_text='Under which column should social media links be placed?', required=False))]))]))]))])), ('contact_info', wagtail.snippets.blocks.SnippetChooserBlock(apps.hip.models.Contact, required=False)), ('button', wagtail.snippets.blocks.SnippetChooserBlock(apps.hip.models.ButtonSnippet, required=False))]))], use_json_field=True),
        ),
    ]

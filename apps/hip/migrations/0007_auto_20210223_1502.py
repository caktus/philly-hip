# Generated by Django 3.1.6 on 2021-02-23 20:02

from django.db import migrations

import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hip', '0006_homepage_contact_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='quick_links',
            field=wagtail.core.fields.StreamField([('quick_links', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='The linked text that will be visible to the reader (maximum of 80 characters)', max_length=80, required=True)), ('link_page', wagtail.core.blocks.PageChooserBlock(help_text='An internal page', required=False)), ('link_url', wagtail.core.blocks.URLBlock(help_text='An external URL (if not linking to an internal page)', max_length=255, required=False)), ('updated_on', wagtail.core.blocks.DateBlock(help_text='If the link is to an external URL, this will be the displayed as the updated date', required=False))]))], blank=True),
        ),
    ]

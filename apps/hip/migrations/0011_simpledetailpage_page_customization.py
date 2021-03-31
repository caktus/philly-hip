# Generated by Django 3.1.6 on 2021-03-31 00:42

from django.db import migrations

import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hip', '0010_simpledetailpage_simpledetailpagecategory_simplelistpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='simpledetailpage',
            name='page_customization',
            field=wagtail.core.fields.StreamField([('disable_right_nav', wagtail.core.blocks.BooleanBlock(help_text='Remove right side navigation from this page?', required=False))], blank=True),
        ),
    ]

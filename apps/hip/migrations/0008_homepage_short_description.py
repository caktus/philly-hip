# Generated by Django 3.1.6 on 2021-03-18 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hip', '0007_auto_20210223_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='short_description',
            field=models.CharField(blank=True, default='', help_text='A short description of the website that will be shown to users when they are on the home page.', max_length=255),
        ),
    ]

# Generated by Django 3.1.8 on 2021-04-20 23:16

from django.db import migrations, models

import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('auth_content', '0009_remove_pcwmsahomepage_action_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='closedpodcontactinformation',
            name='primary_contact_personal_email',
            field=models.EmailField(blank=True, help_text='The personal email of the primary contact', max_length=255, verbose_name='Personal / Home Email'),
        ),
        migrations.AlterField(
            model_name='closedpodcontactinformation',
            name='secondary_contact_cell_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='The cell phone number of the secondary contact', max_length=128, region=None, verbose_name='Cell Phone'),
        ),
        migrations.AlterField(
            model_name='closedpodcontactinformation',
            name='secondary_contact_cell_phone_provider',
            field=models.CharField(blank=True, choices=[('AT&T', 'AT&T'), ('Verizon', 'Verizon'), ('T-Mobile', 'T-Mobile'), ('Dish', 'Dish'), ('Other', 'Other')], help_text='The cell phone provider of the secondary contact', max_length=8, verbose_name='Provider'),
        ),
        migrations.AlterField(
            model_name='closedpodcontactinformation',
            name='secondary_contact_name',
            field=models.CharField(blank=True, help_text='The name of the secondary contact', max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='closedpodcontactinformation',
            name='secondary_contact_personal_email',
            field=models.EmailField(blank=True, help_text='The person email of the secondary contact', max_length=255, verbose_name='Personal / Home Email'),
        ),
        migrations.AlterField(
            model_name='closedpodcontactinformation',
            name='secondary_contact_work_email',
            field=models.EmailField(blank=True, help_text='The work email of the secondary contact', max_length=255, verbose_name='Work Email'),
        ),
    ]
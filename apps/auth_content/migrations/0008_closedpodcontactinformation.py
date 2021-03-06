# Generated by Django 3.1.6 on 2021-04-12 11:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("auth_content", "0007_bigcities_group"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClosedPODContactInformation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "facility_name",
                    models.CharField(max_length=255, verbose_name="Facility Name*"),
                ),
                (
                    "facility_id",
                    models.CharField(max_length=20, verbose_name="Facility ID*"),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None, verbose_name="Phone Number*"
                    ),
                ),
                (
                    "extension",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="Extension"
                    ),
                ),
                (
                    "available_24_7",
                    models.BooleanField(default=False, verbose_name="Available 24/7"),
                ),
                (
                    "special_instructions",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name="Special Instructions for calling this number",
                    ),
                ),
                (
                    "primary_contact_name",
                    models.CharField(
                        help_text="The name of the primary contact",
                        max_length=255,
                        verbose_name="Name*",
                    ),
                ),
                (
                    "primary_contact_work_email",
                    models.EmailField(
                        help_text="The work email of the primary contact",
                        max_length=255,
                        verbose_name="Work Email*",
                    ),
                ),
                (
                    "primary_contact_personal_email",
                    models.CharField(
                        help_text="The personal email of the primary contact",
                        max_length=255,
                        verbose_name="Personal / Home Email*",
                    ),
                ),
                (
                    "primary_contact_cell_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        help_text="The cell phone number of the primary contact",
                        max_length=128,
                        region=None,
                        verbose_name="Cell Phone*",
                    ),
                ),
                (
                    "primary_contact_cell_phone_provider",
                    models.CharField(
                        choices=[
                            ("AT&T", "AT&T"),
                            ("Verizon", "Verizon"),
                            ("T-Mobile", "T-Mobile"),
                            ("Dish", "Dish"),
                            ("Other", "Other"),
                        ],
                        help_text="The cell phone provider of the primary contact",
                        max_length=8,
                        verbose_name="Provider*",
                    ),
                ),
                (
                    "secondary_contact_name",
                    models.CharField(
                        help_text="The name of the secondary contact",
                        max_length=255,
                        verbose_name="Name*",
                    ),
                ),
                (
                    "secondary_contact_work_email",
                    models.EmailField(
                        help_text="The work email of the secondary contact",
                        max_length=255,
                        verbose_name="Work Email*",
                    ),
                ),
                (
                    "secondary_contact_personal_email",
                    models.CharField(
                        help_text="The person email of the secondary contact",
                        max_length=255,
                        verbose_name="Personal / Home Email*",
                    ),
                ),
                (
                    "secondary_contact_cell_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        help_text="The cell phone number of the secondary contact",
                        max_length=128,
                        region=None,
                        verbose_name="Cell Phone*",
                    ),
                ),
                (
                    "secondary_contact_cell_phone_provider",
                    models.CharField(
                        choices=[
                            ("AT&T", "AT&T"),
                            ("Verizon", "Verizon"),
                            ("T-Mobile", "T-Mobile"),
                            ("Dish", "Dish"),
                            ("Other", "Other"),
                        ],
                        help_text="The cell phone provider of the secondary contact",
                        max_length=8,
                        verbose_name="Provider*",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Closed POD Contacts",
            },
        ),
    ]

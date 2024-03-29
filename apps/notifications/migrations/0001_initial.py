# Generated by Django 3.1.8 on 2021-06-10 15:59

import django.core.validators
from django.db import migrations, models

import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="InternalEmployeeAlertSubscriber",
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
                    "first_name",
                    models.CharField(
                        default="", max_length=255, verbose_name="First Name*"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        default="", max_length=255, verbose_name="Last Name*"
                    ),
                ),
                (
                    "professional_license",
                    models.CharField(
                        choices=[
                            ("MD", "Doctor of Medicine"),
                            ("DO", "Doctor of Osteopathic Medicine"),
                            ("NP", "Nurse Practitioner"),
                            ("RN", "Registered Nurse"),
                            ("Other", "Other"),
                        ],
                        max_length=5,
                        verbose_name="Professional License*",
                    ),
                ),
                (
                    "languages_spoken",
                    models.CharField(
                        default="", max_length=255, verbose_name="Languages Spoken*"
                    ),
                ),
                (
                    "division",
                    models.CharField(
                        choices=[
                            (
                                "AIDS Activities Coordinating Office",
                                "AIDS Activities Coordinating Office",
                            ),
                            ("Air Management Services", "Air Management Services"),
                            (
                                "Ambulatory Health Services",
                                "Ambulatory Health Services",
                            ),
                            ("COVID Containment", "COVID Containment"),
                            (
                                "Division of Disease Control",
                                "Division of Disease Control",
                            ),
                            (
                                "Environmental Health Services",
                                "Environmental Health Services",
                            ),
                            ("Finance", "Finance"),
                            ("Get Healthy Philly", "Get Healthy Philly"),
                            (
                                "Health Commissioner's Office",
                                "Health Commissioner's Office",
                            ),
                            ("Human Resources", "Human Resources"),
                            (
                                "Information and Technology",
                                "Information and Technology",
                            ),
                            (
                                "Maternal, Child, and Family Health",
                                "Maternal, Child, and Family Health",
                            ),
                            (
                                "Office of the Medical Examiner",
                                "Office of the Medical Examiner",
                            ),
                            (
                                "Office of Facilities Management",
                                "Office of Facilities Management",
                            ),
                            ("Public Health Laboratory", "Public Health Laboratory"),
                            (
                                "Substance Use Prevention and Harm Reduction",
                                "Substance Use Prevention and Harm Reduction",
                            ),
                        ],
                        max_length=100,
                        verbose_name="Division*",
                    ),
                ),
                (
                    "work_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None, verbose_name="Work Phone*"
                    ),
                ),
                (
                    "work_email",
                    models.EmailField(max_length=254, verbose_name="Work Email*"),
                ),
                (
                    "cell_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None, verbose_name="Cell Phone*"
                    ),
                ),
                (
                    "personal_email",
                    models.EmailField(max_length=254, verbose_name="Personal Email*"),
                ),
                (
                    "home_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None, verbose_name="Home Phone*"
                    ),
                ),
                (
                    "street_address",
                    models.CharField(max_length=255, verbose_name="Street Address*"),
                ),
                ("city", models.CharField(max_length=255, verbose_name="City*")),
                ("state", models.CharField(max_length=255, verbose_name="State*")),
                (
                    "zip_code",
                    models.CharField(
                        default="",
                        max_length=10,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[0-9]{5}(?:-[0-9]{4})?$",
                                "Either provide a 5 or 9 digit zipcode Ex: 12345 or 12345-1234",
                            )
                        ],
                        verbose_name="Zip Code*",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Internal Employee Alerts Subscribers",
            },
        ),
    ]

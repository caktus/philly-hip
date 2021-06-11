from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from apps.health_alerts.utils import zipcode_validator


class InternalEmployeeAlertSubscriber(models.Model):
    """A model to keep track of people subscribe to employee alerts."""

    class DIVISION_CHOICES(models.TextChoices):
        AIDS_ACTIVITIES_COORDINATING_OFFICE = (
            "AIDS Activities Coordinating Office",
            "AIDS Activities Coordinating Office",
        )
        AIR_MANAGEMENT_SERVICES = (
            "Air Management Services",
            "Air Management Services",
        )
        AMBULATORY_HEALTH_SERVICES = (
            "Ambulatory Health Services",
            "Ambulatory Health Services",
        )
        COVID_CONTAINMENT = (
            "COVID Containment",
            "COVID Containment",
        )
        DIVISION_OF_DISEASE_CONTROL = (
            "Division of Disease Control",
            "Division of Disease Control",
        )
        ENVIRONMENTAL_HEALTH_SERVICES = (
            "Environmental Health Services",
            "Environmental Health Services",
        )
        FINANCE = (
            "Finance",
            "Finance",
        )
        GET_HEALTHY_PHILLY = (
            "Get Healthy Philly",
            "Get Healthy Philly",
        )
        HEALTH_COMMISSIONERS_OFFICE = (
            "Health Commissioner's Office",
            "Health Commissioner's Office",
        )
        HUMAN_RESOURCES = (
            "Human Resources",
            "Human Resources",
        )
        INFORMATION_AND_TECHNOLOGY = (
            "Information and Technology",
            "Information and Technology",
        )
        MATERNAL_CHILD_AND_FAMILY_HEALTH = (
            "Maternal, Child, and Family Health",
            "Maternal, Child, and Family Health",
        )
        OFFICE_OF_THE_MEDICAL_EXAMINER = (
            "Office of the Medical Examiner",
            "Office of the Medical Examiner",
        )
        OFFICE_OF_FACILITIES_MANAGEMENT = (
            "Office of Facilities Management",
            "Office of Facilities Management",
        )
        PUBLIC_HEALTH_LABORATORY = (
            "Public Health Laboratory",
            "Public Health Laboratory",
        )
        SUBSTANCE_USE_PREVENTION_AND_HARM_REDUCTION = (
            "Substance Use Prevention and Harm Reduction",
            "Substance Use Prevention and Harm Reduction",
        )

    class PROFESSIONAL_LICENSE_CHOICES(models.TextChoices):
        DOCTOR_OF_MEDICINE = (
            "MD",
            "Doctor of Medicine",
        )
        DOCTOR_OF_OSTEOPATHIC_MEDINCE = (
            "DO",
            "Doctor of Osteopathic Medicine",
        )
        NURSE_PRACTITIONER = (
            "NP",
            "Nurse Practitioner",
        )
        REGISTERED_NURSE = (
            "RN",
            "Registered Nurse",
        )
        OTHER = (
            "Other",
            "Other",
        )

    first_name = models.CharField(
        "First Name*",
        max_length=255,
        default="",
    )
    last_name = models.CharField(
        "Last Name*",
        max_length=255,
        default="",
    )
    professional_license = models.CharField(
        "Professional License*",
        max_length=5,
        choices=PROFESSIONAL_LICENSE_CHOICES.choices,
    )
    languages_spoken = models.CharField("Languages Spoken*", max_length=255, default="")
    division = models.CharField(
        "Division*",
        max_length=100,
        choices=DIVISION_CHOICES.choices,
    )

    work_phone = PhoneNumberField("Work Phone*")
    work_email = models.EmailField("Work Email*")
    cell_phone = PhoneNumberField("Cell Phone*")
    personal_email = models.EmailField("Personal Email*")
    home_phone = PhoneNumberField("Home Phone*")
    street_address = models.CharField("Street Address*", max_length=255)
    city = models.CharField("City*", max_length=255)
    state = models.CharField("State*", max_length=255)
    zip_code = models.CharField(
        "Zip Code*", max_length=10, default="", validators=[zipcode_validator]
    )

    class Meta:
        verbose_name_plural = "Internal Employee Alerts Subscribers"

    def __str__(self):
        return (
            f"Internal Employee Alerts Subscriber: {self.first_name} {self.last_name}"
        )

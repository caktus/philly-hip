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

    class AMBULATORY_HEALTH_CENTER_CHOICES(models.TextChoices):
        ADMINISTRATION = ("Administration", "Administration")
        HEALTH_CENTER_2 = ("Health Center 2", "Health Center 2")
        HEALTH_CENTER_3 = ("Health Center 3", "Health Center 3")
        HEALTH_CENTER_4 = ("Health Center 4", "Health Center 4")
        HEALTH_CENTER_5 = ("Health Center 5", "Health Center 5")
        HEALTH_CENTER_6 = ("Health Center 6", "Health Center 6")
        HEALTH_CENTER_9 = ("Health Center 9", "Health Center 9")
        HEALTH_CENTER_10 = ("Health Center 10", "Health Center 10")
        HEALTH_CENTER_SM = (
            "Health Center Strawberry Mansion",
            "Health Center Strawberry Mansion",
        )

    class EHS_PROGRAM_CHOICES(models.TextChoices):
        ADMINISTRATION = ("Administration", "Administration")
        ENVIRONMENTAL_ENGINEERING = (
            "Environmental Engineering",
            "Environmental Engineering",
        )
        FOOD_PROTECTION = ("Food Protection", "Food Protection")
        VECTOR_CONTROL = ("Vector Control", "Vector Control")
        CHILDHOOD_LEAD = ("Childhood Lead", "Childhood Lead")

    class DISEASE_CONTROL_PROGRAM_CHOICES(models.TextChoices):
        ADMINISTRATION = ("Administration", "Administration")
        ACUTE_COMMUNICABLE_DISEASE = (
            "Acute Communicable Disease",
            "Acute Communicable Disease",
        )
        BIOTERRORISM = ("Bioterrorism", "Bioterrorism")
        EPIDEMIOLOGY = ("Epidemiology", "Epidemiology")
        HEALTH_CENTER_1 = ("Health Center 1", "Health Center 1")
        HEALTH_CENTER_5 = ("Health Center 5", "Health Center 5")
        IMMUNIZATIONS = ("Immunizations", "Immunizations")
        STD_CONTROL = ("STD Control", "STD Control")
        SUPPORT_STAFF = ("Support Staff", "Support Staff")
        TUBERCULOSIS = ("Tuberculosis", "Tuberculosis")
        HEPATITIS = ("Hepatitis", "Hepatitis")
        HAI_AR = ("HAI-AR", "HAI-AR")

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
    ambulatory_health_center = models.CharField(
        "Ambulatory Health Center*",
        max_length=100,
        blank=True,
        choices=AMBULATORY_HEALTH_CENTER_CHOICES.choices,
    )
    ehs_program = models.CharField(
        "EHS Program*",
        max_length=100,
        blank=True,
        choices=EHS_PROGRAM_CHOICES.choices,
    )
    disease_control_program = models.CharField(
        "Disease Control Program*",
        max_length=100,
        blank=True,
        choices=DISEASE_CONTROL_PROGRAM_CHOICES.choices,
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


class CommunityResponseSubscriber(models.Model):
    """A model to keep track of people who subscribe to community alerts."""

    class COMMUNITY_MEMBERS_CHOICES(models.TextChoices):
        CHILDREN_YOUTH = (
            "Children/Youth",
            "Children/Youth",
        )
        OLDER_ADULTS = (
            "Older Adults",
            "Older Adults",
        )
        MARGINALIZED_RACIAL_OR_ETHNIC_GROUP = (
            "Marginalized racial or ethnic group",
            "Marginalized racial or ethnic group",
        )
        IMMIGRANT = (
            "Immigrant",
            "Immigrant",
        )
        REFUGEE_OR_UNDOCUMENTED_COMMUNITIES = (
            "refugee or undocumented communities",
            "refugee or undocumented communities",
        )
        GENDER_NON_CONFORMING_NON_BINARY = (
            "Gender non-conforming/non-binary",
            "Gender non-conforming/non-binary",
        )
        LGBTQ_PLUS = (
            "LGBTQ+",
            "LGBTQ+",
        )
        UNEMPLOYED = (
            "Unemployed",
            "Unemployed",
        )
        UNINSURED_UNDERINSURED = (
            "Uninsured/Underinsured",
            "Uninsured/Underinsured",
        )
        EXPERIENCING_HOMELESSNESS = (
            "Experiencing homelessness",
            "Experiencing homelessness",
        )
        LOW_INCOME_COMMUNITIES = (
            "Low-income communities",
            "Low-income communities",
        )
        PEOPLE_WITH_DISABILITIES = (
            "People with disabilities",
            "People with disabilities",
        )
        PEOPLE_WHO_ARE_HOMEBOUND = (
            "People who are homebound",
            "People who are homebound",
        )
        LIVING_WITH_A_MENTAL_ILLNESS = (
            "Living with a mental illness",
            "Living with a mental illness",
        )
        LIVING_WITH_A_SUBSTANCE_USE_DISORDER = (
            "Living with a substance use disorder",
            "Living with a substance use disorder",
        )
        CHRONICALLY_ILL = (
            "Chronically ill",
            "Chronically ill",
        )
        RETURNING_CITIZENS = (
            "Returning citizens",
            "Returning citizens",
        )
        CURRENTLY_INCARCERATED = (
            "Currently incarcerated",
            "Currently incarcerated",
        )
        FAITH_COMMUNITIES = (
            "Faith communities",
            "Faith communities",
        )
        MINIMAL_TO_NO_DIGITAL_ACCESS = (
            "Minimal to no digital access",
            "Minimal to no digital access",
        )
        PREGNANT = (
            "Pregnant",
            "Pregnant",
        )
        SINGLE_PARENT = (
            "Single parent",
            "Single parent",
        )
        VETERANS = (
            "Veterans",
            "Veterans",
        )
        LIMITED_ENGLISH_PROFICIENT = (
            "Limited English proficient",
            "Limited English proficient",
        )
        CAREGIVER_DEPENDENT = (
            "Caregiver dependent",
            "Caregiver dependent",
        )
        NO_ACCESS_TO_PRIVATE_VEHICLE = (
            "No access to private vehicle",
            "No access to private vehicle",
        )
        DEPENDENT_ON_PRESCRIPTION_MEDICATIONS = (
            "Dependent on prescription medications",
            "Dependent on prescription medications",
        )
        LIVING_IN_A_CONGREGATE_SETTING = (
            "Living in a congregate setting",
            "Living in a congregate setting",
        )
        STUDENTS = (
            "Students",
            "Students",
        )
        SURVIVORS_OF_VIOLENCE_OR_ABUSE = (
            "Survivors of violence or abuse",
            "Survivors of violence or abuse",
        )
        ESSENTIAL_WORKER = (
            "Essential worker",
            "Essential worker",
        )
        GENERAL_PUBLIC = (
            "General public",
            "General public",
        )
        OTHER = (
            "Other",
            "Other",
        )
        ALL_OF_THESE = (
            "All of these",
            "All of these",
        )

    class ORGANIZATION_TYPE_CHOICES(models.TextChoices):
        ARTS_CULTURE = (
            (
                "Arts and Culture",
                "Arts and Culture",
            ),
        )
        BLOCK_CAPTAIN = (
            (
                "Block Captain",
                "Block Captain",
            ),
        )
        CIVIC_ENGAGEMENT_ELECTED_OFFICIAL = (
            (
                "Civic Engagement/Elected Official",
                "Civic Engagement/Elected Official",
            ),
        )
        DISABILITIES_ACCESS_FUNCTIONAL_NEEDS = (
            (
                "Disabilities and Access and Functional Needs",
                "Disabilities and Access and Functional Needs",
            ),
        )
        EDUCATION = (
            (
                "Education (Schools/Colleges/Universities)",
                "Education (Schools/Colleges/Universities)",
            ),
        )
        FREE_LIBRARY_OF_PHILADELPHIA = (
            (
                "Free Library of Philadelphia",
                "Free Library of Philadelphia",
            ),
        )
        GENERAL_COMMUNITY_SERVICES = (
            (
                "General Community Services",
                "General Community Services",
            ),
        )
        HEALTHCARE = (
            (
                "Healthcare",
                "Healthcare",
            ),
        )
        IMMIGRANT_REFUGEE_COMMUNITIES = (
            (
                "Immigrante/Refugee/Communities that speak languages other than English",
                "Immigrante/Refugee/Communities that speak languages other than English",
            ),
        )
        LIVE_BIRD_MARKET = (
            (
                "Live Bird Market",
                "Live Bird Market",
            ),
        )
        MENTAL_BEHAVIORAL_HEALTH = (
            (
                "Mental/Behavioral Health",
                "Mental/Behavioral Health",
            ),
        )
        OLDER_ADULTS = (
            (
                "Older Adults",
                "Older Adults",
            ),
        )
        HOUSING_HOMELESS_SERVICES = (
            (
                "Housing/Homeless Services",
                "Housing/Homeless Services",
            ),
        )
        RCO_CDC_NAC = (
            (
                "RCO/CDC/NAC",
                "RCO/CDC/NAC",
            ),
        )
        RECREATIONAL = (
            (
                "Recreational",
                "Recreational",
            ),
        )
        RELIGIOUS_FAITH_BASED = (
            (
                "Religious/Faith-based",
                "Religious/Faith-based",
            ),
        )
        WORKERS = (
            (
                "Workers",
                "Workers",
            ),
        )
        YOUTH = (
            (
                "Youth",
                "Youth",
            ),
        )
        UNAFFILIATED_COMMUNITY_LEADER = (
            (
                "Unaffiliated Community Leader",
                "Unaffiliated Community Leader",
            ),
        )

    first_name = models.CharField(
        "First Name",
        max_length=255,
        default="",
    )
    last_name = models.CharField(
        "Last Name",
        max_length=255,
        default="",
    )
    organization_name = models.CharField(
        "Organization Name*",
        max_length=255,
        default="",
    )
    # title = models.CharField(
    #     "Title/Position*",
    #     max_length=255,
    #     default="",
    # )

    email_address = models.EmailField("Email Address*")
    cell_phone = PhoneNumberField("Cell Phone")

    organization_type = models.CharField(
        "Organization Type*",
        max_length=150,
        default="",
        choices=ORGANIZATION_TYPE_CHOICES.choices,
        blank=True,
    )
    organization_zip_code = models.CharField(
        "Zip Code of Organization*",
        max_length=10,
        default="",
        validators=[zipcode_validator],
    )
    organization_community_members_served = models.CharField(
        "Community Members Served",
        max_length=100,
        choices=COMMUNITY_MEMBERS_CHOICES.choices,
    )

    organization_mission_statement = models.CharField(
        "Mission Statement",
        max_length=255,
        default="",
    )

    class Meta:
        verbose_name_plural = "Community Response Subscribers"

    def __str__(self):
        return (
            f"Community Response Network Subscriber: {self.first_name} {self.last_name}"
        )


class DrugOverdoseSubscriber(models.Model):
    """A model to keep track of people who subscribe to drug overdose notifications."""

    class NOTIFICATION_GROUP_CHOICES(models.TextChoices):
        AGENCIES = ("Agencies", "Agencies")
        HOSPITALS = ("Hospitals", "Hospitals")
        COMMUNITY_MEMBERS = ("Community Members", "Community Members")
        MEDIA_PRESS = ("Media/Press", "Media/Press")

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
    medical_specialty = models.CharField(
        "Medical Specialty/Area of Expertise*",
        max_length=255,
        default="",
    )

    company_name = models.CharField(
        "Company Name*",
        max_length=255,
        default="",
    )
    title = models.CharField(
        "Your Title/Position*",
        max_length=255,
        default="",
    )
    work_phone = PhoneNumberField("Work Phone*")

    notification_group = models.CharField(
        "Notification Group*",
        max_length=100,
        choices=NOTIFICATION_GROUP_CHOICES.choices,
    )

    email_address = models.EmailField("Email Address*")
    mobile_phone = PhoneNumberField("Mobile Phone*")

    class Meta:
        verbose_name_plural = "Drug Overdose Subscribers"

    def __str__(self):
        return (
            f"Drug Overdose Notification Subscriber: {self.first_name} {self.last_name}"
        )


class CodeRedCodeBlueSubscriber(models.Model):
    """A model to keep track of people who subscribe to Code Red/Code Blue notifications."""

    first_name = models.CharField(
        "First Name",
        max_length=255,
        blank=True,
    )
    last_name = models.CharField(
        "Last Name",
        max_length=255,
        blank=True,
    )
    agency_name = models.CharField(
        "Agency Name",
        max_length=255,
        blank=True,
    )

    work_phone = PhoneNumberField("Work Phone", blank=True)
    work_email = models.EmailField("Work Email", blank=True)
    cell_phone = PhoneNumberField("Cell Phone", blank=True)
    personal_email = models.EmailField("Personal Email", blank=True)

    class Meta:
        verbose_name_plural = "Code Red/Code Blue Subscribers"

    def __str__(self):
        return f"Code Red/Code Blue Notification Subscriber: {self.first_name} {self.last_name}"


class PublicHealthPreparednessSubscriber(models.Model):
    """A model to keep track of people who subscribe to public health preparedness notifications."""

    class OUTREACH_REQUEST_CHOICES(models.TextChoices):
        MEETING = ("Meeting", "Meeting")
        TRAINING = ("Training", "Training")
        RESOURCE = ("Resource", "Resource")

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
    phone_number = PhoneNumberField("Phone Number*")
    email_address = models.EmailField("Email Address*")

    organization_name = models.CharField(
        "Organization Name*",
        max_length=255,
        default="",
    )
    organization_zip_code = models.CharField(
        "Organization Zip Code*",
        max_length=10,
        default="",
        validators=[zipcode_validator],
    )

    outreach_request_choice = models.CharField(
        "I would like to request a*",
        max_length=10,
        choices=OUTREACH_REQUEST_CHOICES.choices,
    )
    outreach_request_additional_info = models.TextField(
        "Please provide additional information about your request below.",
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Public Health Preparedness Subscribers"

    def __str__(self):
        return (
            f"Public Health Preparedness Subscriber: {self.first_name} {self.last_name}"
        )

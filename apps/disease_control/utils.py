from .models import DiseaseControlPage


def get_topic_specific_guidance_qs():
    return DiseaseControlPage.objects.live().filter(page_type=1)


def get_facility_specific_guidance_qs():
    return DiseaseControlPage.objects.live().filter(page_type=2)


def get_disease_control_services_qs():
    return DiseaseControlPage.objects.live().filter(page_type=3)

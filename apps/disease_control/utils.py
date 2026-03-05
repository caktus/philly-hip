from .models import DiseaseControlPage


def get_topic_specific_guidance_qs():
    return DiseaseControlPage.objects.live().filter(page_type=1).order_by("title")


def get_facility_specific_guidance_qs():
    return DiseaseControlPage.objects.live().filter(page_type=2).order_by("title")


def get_disease_control_services_qs():
    return DiseaseControlPage.objects.live().filter(page_type=3).order_by("title")


def get_visible_section_headers():
    headers = []
    if get_topic_specific_guidance_qs().exists():
        headers.append("Topic-specific Guidance")
    if get_facility_specific_guidance_qs().exists():
        headers.append("Facility-specific Guidance")
    if get_disease_control_services_qs().exists():
        headers.append("Disease Control Services")
    return headers

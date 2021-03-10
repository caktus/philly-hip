from .models import DiseaseControlDetailPage


def get_topic_specific_guidance_qs():
    return DiseaseControlDetailPage.objects.live().filter(page_type=1).order_by("title")


def get_facility_specific_guidance_qs():
    return DiseaseControlDetailPage.objects.live().filter(page_type=2).order_by("title")


def get_disease_control_services_qs():
    return DiseaseControlDetailPage.objects.live().filter(page_type=3).order_by("title")


def get_visible_section_headers():
    return [
        "Topic-specific Guidance" if get_topic_specific_guidance_qs().exists() else "",
        "Facility-specific Guidance"
        if get_facility_specific_guidance_qs().exists()
        else "",
        "Disease Control Services"
        if get_disease_control_services_qs().exists()
        else "",
    ]

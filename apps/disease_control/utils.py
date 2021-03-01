from .models import DiseaseControlPage


def get_topic_specific_guidance_qs():
    return DiseaseControlPage.objects.live().filter(page_type=1)


def get_facility_specific_guidance_qs():
    return DiseaseControlPage.objects.live().filter(page_type=2)


def get_disease_control_services_qs():
    return DiseaseControlPage.objects.live().filter(page_type=3)


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

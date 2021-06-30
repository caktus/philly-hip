from django import template

from ..models import Contact


register = template.Library()


# Advert snippets
@register.inclusion_tag("tags/contact_info.html", takes_context=True)
def contact_info(context):
    return {
        "contact_info": Contact.objects.all(),
        "request": context["request"],
    }

from django import template


register = template.Library()


@register.filter("widget_class")
def widget_class(field):
    return field.field.widget.__class__.__name__

from django.db.models import CharField, F, Value

from wagtail.core.models import Page


def get_most_recent_objects(pages_qs=None, object_count=10):
    """
    Return the most recently updated objects from a number of models.

    Currently, we return the most recently updated models from:
     - Pages

    In order to make it easier to get data from each returned object (in a template),
    several fields are annotated on each object:
     - name
     - updated_at
     - type_of_object
     - model_name
    Note: objects are returned in a list. It is also possible to combine querysets
    together using queryset.union(), but it is difficult to do so for different
    models without using .values(), which means that each object in the queryset
    loses its methods. In order to preserve the methods, objects are combined in
    a list.
    """
    if pages_qs is None:
        pages_qs = Page.objects.live()
    # Get the most recent Page objects.
    pages = (
        pages_qs.exclude(latest_revision_created_at__isnull=True)
        .annotate(
            name=F("title"),
            updated_at=F("latest_revision_created_at"),
            type_of_object=Value("PAGE", output_field=CharField()),
            model_name=Value("page", output_field=CharField()),
        )
        .order_by("-updated_at")
    )

    # Return only the most recent object_count amount of objects.
    return list(pages)[:object_count]

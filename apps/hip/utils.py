from django.db.models import Case, CharField, F, Value, When

from wagtail.core.models import Page
from wagtail.documents.models import Document


def get_most_recent_objects(object_count=10):
    """
    Return the most recently updated objects from a number of models.

    Currently, we return the most recently updated models from:
     - Pages
     - Documents

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
    # Get the most recent Page objects.
    pages = (
        Page.objects.live()
        .exclude(latest_revision_created_at__isnull=True)
        .annotate(
            name=F("title"),
            updated_at=F("latest_revision_created_at"),
            type_of_object=Value("PAGE", output_field=CharField()),
            model_name=Value("page", output_field=CharField()),
        )[:object_count]
    )
    # Get the most recent Document objects.
    documents = Document.objects.annotate(
        name=F("title"),
        updated_at=F("created_at"),
        type_of_object=Case(
            When(file__endswith="jpg", then=Value("JPG", output_field=CharField())),
            When(file__endswith="png", then=Value("PNG", output_field=CharField())),
            When(file__endswith="pdf", then=Value("PDF", output_field=CharField())),
        ),
        model_name=Value("document", output_field=CharField()),
    )[:object_count]

    # Sort the combined_list by their 'updated_at' property.
    combined_list = list(pages) + list(documents)
    combined_list.sort(key=lambda x: x.updated_at, reverse=True)

    # Return only the most recent object_count amount of objects.
    return combined_list[:object_count]

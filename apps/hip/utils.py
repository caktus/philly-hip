from django.db.models import CharField, F, Value

from pdfid import pdfid
from wagtail.models import Page


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


def scan_pdf_for_malicious_content(pdf_file_path):
    """
    Scan the pdf_file_path for malicious content, using PDFiD.

    If the file is either not a valid PDF file or has malicious content, we
    raise an error.
    """
    # Set the options for scanning the PDF.
    options = pdfid.get_fake_options()  # sets all options to False
    options.scan = True
    options.json = True  # JSON output
    options.verbose = True  # raise exceptions when they occur

    # Scan the PDF file, and get the results.
    scan_results = pdfid.PDFiDMain([pdf_file_path], options)

    # Inspect the results of the scan, and raise errors if the file is not valid
    # or if the file is suspicious.
    if not scan_results or not scan_results["reports"]:
        raise Exception("Invalid PDF")
    elif scan_results["reports"][0].get("/Page", 0) < 1:
        raise Exception("Invalid PDF")
    else:
        # The PDF has JavaScript if the '/JS' count or the '/JavaScript' count is greater than 0.
        has_js = (
            scan_results["reports"][0].get("/JS") > 0
            or scan_results["reports"][0].get("/JavaScript") > 0
        )
        # Does the PDF have an automatic action that is to be performed when it
        # is viewed (without user interaction)?
        has_automatic_action = scan_results["reports"][0].get("/AA") > 0
        # Does the PDF have an action that is to be performed when it is opened
        # (without user interaction)?
        has_open_action = scan_results["reports"][0].get("/OpenAction") > 0

        # If the PDF has JavaScript and an open action or an automatic action,
        # then reject it.
        if has_js and (has_automatic_action or has_open_action):
            raise Exception("This PDF file has suspicious content.")

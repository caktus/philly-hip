# Generated manually to replace DiseaseAndConditionDetailPage content fields
# with a StreamField, migrating both live DB rows AND Wagtail revision JSON.

import uuid

from django.db import migrations

import wagtail.fields

import apps.disease_control.models


SECTION_FIELD_NAMES = (
    "description",
    "at_a_glance",
    "current_recommendations",
    "surveillance",
    "vaccine_info",
    "diagnosis_info",
    "provider_resources",
)


def _stream_block(block_type, value):
    return {
        "type": block_type,
        "value": str(value),
        "id": str(uuid.uuid4()),
    }


def forwards(apps, schema_editor):
    DiseaseAndConditionDetailPage = apps.get_model(
        "disease_control", "DiseaseAndConditionDetailPage"
    )
    ContentType = apps.get_model("contenttypes", "ContentType")
    Revision = apps.get_model("wagtailcore", "Revision")

    # --- 1. Migrate live DB rows ---
    for page in DiseaseAndConditionDetailPage.objects.all():
        content_sections = []
        for field_name in SECTION_FIELD_NAMES:
            value = str(getattr(page, field_name) or "")
            content_sections.append(_stream_block(field_name, value))

        page.content_sections = content_sections
        page.save(update_fields=["content_sections"])

    # --- 2. Migrate Wagtail revisions ---
    ct = ContentType.objects.get_for_model(DiseaseAndConditionDetailPage)
    revisions = Revision.objects.filter(content_type=ct)

    for revision in revisions:
        content = revision.content

        # Skip if already converted
        if "content_sections" in content:
            continue

        # Check if any of the old field names exist
        has_old_fields = any(field in content for field in SECTION_FIELD_NAMES)
        if not has_old_fields:
            continue

        # Build the StreamField JSON from the old fields
        content_sections = []
        for field_name in SECTION_FIELD_NAMES:
            value = content.pop(field_name, "") or ""
            content_sections.append(_stream_block(field_name, str(value)))

        content["content_sections"] = content_sections
        revision.content = content
        revision.save(update_fields=["content"])


def backwards(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Revision = apps.get_model("wagtailcore", "Revision")
    DiseaseAndConditionDetailPage = apps.get_model(
        "disease_control", "DiseaseAndConditionDetailPage"
    )

    ct = ContentType.objects.get_for_model(DiseaseAndConditionDetailPage)
    revisions = Revision.objects.filter(content_type=ct)

    for revision in revisions:
        content = revision.content

        if "content_sections" not in content:
            continue

        # Restore old fields from the StreamField JSON
        content_sections = content.pop("content_sections", [])
        for block in content_sections:
            block_type = block.get("type")
            if block_type in SECTION_FIELD_NAMES:
                content[block_type] = block.get("value", "")

        revision.content = content
        revision.save(update_fields=["content"])


class Migration(migrations.Migration):

    dependencies = [
        ("disease_control", "0018_alter_diseasecontrolchildstaticpage_body"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("wagtailcore", "0094_alter_page_locale"),
    ]

    operations = [
        migrations.AddField(
            model_name="diseaseandconditiondetailpage",
            name="content_sections",
            field=wagtail.fields.StreamField(
                [
                    ("description", 0),
                    ("at_a_glance", 1),
                    ("current_recommendations", 2),
                    ("surveillance", 3),
                    ("vaccine_info", 4),
                    ("diagnosis_info", 5),
                    ("provider_resources", 6),
                ],
                blank=True,
                block_lookup={
                    0: ("apps.disease_control.blocks.DescriptionBlock", (), {}),
                    1: ("apps.disease_control.blocks.AtAGlanceBlock", (), {}),
                    2: (
                        "apps.disease_control.blocks.CurrentRecommendationsBlock",
                        (),
                        {},
                    ),
                    3: ("apps.disease_control.blocks.SurveillanceBlock", (), {}),
                    4: ("apps.disease_control.blocks.VaccineInfoBlock", (), {}),
                    5: ("apps.disease_control.blocks.DiagnosisInfoBlock", (), {}),
                    6: ("apps.disease_control.blocks.ProviderResourcesBlock", (), {}),
                },
                default=apps.disease_control.models.default_disease_detail_content_sections,
            ),
        ),
        migrations.RunPython(forwards, backwards),
        migrations.RemoveField(
            model_name="diseaseandconditiondetailpage",
            name="description",
        ),
        migrations.RemoveField(
            model_name="diseaseandconditiondetailpage",
            name="at_a_glance",
        ),
        migrations.RemoveField(
            model_name="diseaseandconditiondetailpage",
            name="current_recommendations",
        ),
        migrations.RemoveField(
            model_name="diseaseandconditiondetailpage",
            name="surveillance",
        ),
        migrations.RemoveField(
            model_name="diseaseandconditiondetailpage",
            name="vaccine_info",
        ),
        migrations.RemoveField(
            model_name="diseaseandconditiondetailpage",
            name="diagnosis_info",
        ),
        migrations.RemoveField(
            model_name="diseaseandconditiondetailpage",
            name="provider_resources",
        ),
    ]

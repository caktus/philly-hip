# Generated by Django 3.1.6 on 2021-04-05 13:01

from django.db import migrations


def create_bigcities_group(apps, schema_editor):
    """Create a 'Big Cities' Group."""
    Group = apps.get_model("auth", "Group")
    Group.objects.create(name="Big Cities")


def delete_bigcities_group(apps, schema_editor):
    """Delete a 'Big Cities' Group, if it exists."""
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name="Big Cities").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("auth_content", "0006_bigcitieshomepage"),
    ]

    operations = [migrations.RunPython(create_bigcities_group, delete_bigcities_group)]

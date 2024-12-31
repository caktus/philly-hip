# Generated by Django 3.2.23 on 2024-12-31 05:42

from django.db import migrations, models

import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0008_coderedcodebluesubscriber_fields_are_optional'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communityresponsesubscriber',
            name='organization_po_box',
        ),
        migrations.RemoveField(
            model_name='communityresponsesubscriber',
            name='organization_street_address',
        ),
        migrations.RemoveField(
            model_name='communityresponsesubscriber',
            name='organization_zip_codes_served',
        ),
        migrations.RemoveField(
            model_name="communityresponsesubscriber",
            name="title",
        ),
        migrations.AddField(
            model_name='communityresponsesubscriber',
            name='organization_mission_statement',
            field=models.CharField(default='', max_length=255, verbose_name='Mission Statement'),
        ),
        migrations.AddField(
            model_name='communityresponsesubscriber',
            name='organization_type',
            field=models.CharField(blank=True, choices=[("('Arts and Culture', 'Arts and Culture')", 'Arts Culture'), ("('Block Captain', 'Block Captain')", 'Block Captain'), ("('Civic Engagement/Elected Official', 'Civic Engagement/Elected Official')", 'Civic Engagement Elected Official'), ("('Disabilities and Access and Functional Needs', 'Disabilities and Access and Functional Needs')", 'Disabilities Access Functional Needs'), ("('Education (Schools/Colleges/Universities)', 'Education (Schools/Colleges/Universities)')", 'Education'), ("('Free Library of Philadelphia', 'Free Library of Philadelphia')", 'Free Library Of Philadelphia'), ("('General Community Services', 'General Community Services')", 'General Community Services'), ("('Healthcare', 'Healthcare')", 'Healthcare'), ("('Immigrante/Refugee/Communities that speak languages other than English', 'Immigrante/Refugee/Communities that speak languages other than English')", 'Immigrant Refugee Communities'), ("('Live Bird Market', 'Live Bird Market')", 'Live Bird Market'), ("('Mental/Behavioral Health', 'Mental/Behavioral Health')", 'Mental Behavioral Health'), ("('Older Adults', 'Older Adults')", 'Older Adults'), ("('Housing/Homeless Services', 'Housing/Homeless Services')", 'Housing Homeless Services'), ("('RCO/CDC/NAC', 'RCO/CDC/NAC')", 'Rco Cdc Nac'), ("('Recreational', 'Recreational')", 'Recreational'), ("('Religious/Faith-based', 'Religious/Faith-based')", 'Religious Faith Based'), ("('Workers', 'Workers')", 'Workers'), ("('Youth', 'Youth')", 'Youth'), ("('Unaffiliated Community Leader', 'Unaffiliated Community Leader')", 'Unaffiliated Community Leader')], default='', max_length=150, verbose_name='Organization Type*'),
        ),
        migrations.AlterField(
            model_name='communityresponsesubscriber',
            name='cell_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Cell Phone'),
        ),
        migrations.AlterField(
            model_name='communityresponsesubscriber',
            name='first_name',
            field=models.CharField(default='', max_length=255, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='communityresponsesubscriber',
            name='last_name',
            field=models.CharField(default='', max_length=255, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='communityresponsesubscriber',
            name='organization_community_members_served',
            field=models.CharField(choices=[('Children/Youth', 'Children/Youth'), ('Older Adults', 'Older Adults'), ('Marginalized racial or ethnic group', 'Marginalized racial or ethnic group'), ('Immigrant', 'Immigrant'), ('refugee or undocumented communities', 'refugee or undocumented communities'), ('Gender non-conforming/non-binary', 'Gender non-conforming/non-binary'), ('LGBTQ+', 'LGBTQ+'), ('Unemployed', 'Unemployed'), ('Uninsured/Underinsured', 'Uninsured/Underinsured'), ('Experiencing homelessness', 'Experiencing homelessness'), ('Low-income communities', 'Low-income communities'), ('People with disabilities', 'People with disabilities'), ('People who are homebound', 'People who are homebound'), ('Living with a mental illness', 'Living with a mental illness'), ('Living with a substance use disorder', 'Living with a substance use disorder'), ('Chronically ill', 'Chronically ill'), ('Returning citizens', 'Returning citizens'), ('Currently incarcerated', 'Currently incarcerated'), ('Faith communities', 'Faith communities'), ('Minimal to no digital access', 'Minimal to no digital access'), ('Pregnant', 'Pregnant'), ('Single parent', 'Single parent'), ('Veterans', 'Veterans'), ('Limited English proficient', 'Limited English proficient'), ('Caregiver dependent', 'Caregiver dependent'), ('No access to private vehicle', 'No access to private vehicle'), ('Dependent on prescription medications', 'Dependent on prescription medications'), ('Living in a congregate setting', 'Living in a congregate setting'), ('Students', 'Students'), ('Survivors of violence or abuse', 'Survivors of violence or abuse'), ('Essential worker', 'Essential worker'), ('General public', 'General public'), ('Other', 'Other'), ('All of these', 'All of these')], max_length=100, verbose_name='Community Members Served'),
        ),
    ]

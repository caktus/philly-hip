import pytest

from ..forms import (
    CodeRedCodeBlueSubscriberForm,
    CommunityResponseSubscriberForm,
    InternalAlertsSubscriberForm,
    OpioidOverdoseSubscriberForm,
    PublicHealthPreparednessSubscriberForm,
)


@pytest.mark.parametrize(
    "form_class",
    [
        CodeRedCodeBlueSubscriberForm,
        CommunityResponseSubscriberForm,
        InternalAlertsSubscriberForm,
        OpioidOverdoseSubscriberForm,
        PublicHealthPreparednessSubscriberForm,
    ],
)
def test_asterisks_mark_required_fields(db, form_class):
    """Required field names end with an asterisk."""
    form = form_class()
    for field_name in form.fields:
        # A few fields are optional at the database level, and are not initially
        # visible to the user, but become visible and required if the user selects
        # a certain value for another field. As a result, these fields have an
        # asterisk in their name, but do not have the "required" attribute
        # set to True.
        excluded_fields = []
        if form_class == InternalAlertsSubscriberForm:
            excluded_fields = [
                "ambulatory_health_center",
                "ehs_program",
                "disease_control_program",
            ]

        if field_name not in excluded_fields:
            if form.fields[field_name].required:
                assert form.fields[field_name].label.endswith("*") is True
            else:
                assert form.fields[field_name].label.endswith("*") is False


def test_form_valid_internal_alert_form(db, internal_alert_data):
    """Test putting valid data into the form."""
    form = InternalAlertsSubscriberForm(internal_alert_data)
    assert form.is_valid()


def test_invalid_phone_number_internal_alert_form(db, internal_alert_data):
    """Having invalid data means the form is not valid."""
    # The 'work_phone' field value is not valid.
    internal_alert_data["work_phone"] = "0"

    form = InternalAlertsSubscriberForm(internal_alert_data)

    assert form.is_valid() is False
    expected_error = (
        "Enter a valid phone number (e.g. (201) 555-0123) or a number "
        "with an international call prefix."
    )
    assert {"work_phone": [expected_error]} == form.errors


def test_invalid_zip_code_internal_alert_form(db, internal_alert_data):
    """Having invalid data means the form is not valid."""
    # The 'zip_code' field value is not valid.
    internal_alert_data["zip_code"] = "1234"

    form = InternalAlertsSubscriberForm(internal_alert_data)

    assert form.is_valid() is False
    expected_error = "Either provide a 5 or 9 digit zipcode Ex: 12345 or 12345-1234"
    assert {"zip_code": [expected_error]} == form.errors


@pytest.mark.parametrize(
    "division_value,expected_required_field,valid_required_field_value",
    [
        ("Ambulatory Health Services", "ambulatory_health_center", "Administration"),
        ("Division of Disease Control", "disease_control_program", "Administration"),
        ("Environmental Health Services", "ehs_program", "Administration"),
    ],
)
def test_internal_alert_form_division(
    db,
    internal_alert_data,
    division_value,
    expected_required_field,
    valid_required_field_value,
):
    """
    The "division" field can have a value that requires other fields to be present.

    If a user chooses the "Ambulatory Health Services" division, then the user must
    also fill in the "ambulatory_health_center" field.
    If a user chooses the "Division of Disease Control" division, then the user must
    also fill in the "disease_control_program" field.
    If a user chooses the "Environmental Health Services" division, then the user must
    also fill in the "ehs_program" field.
    """
    # The expected_required_field does not have a value in the internal_alert_data.
    if expected_required_field in internal_alert_data:
        internal_alert_data.pop(expected_required_field)

    # Set a value for the "division" field which will not require any more fields
    # to be present.
    internal_alert_data["division"] = "Get Healthy Philly"
    form = InternalAlertsSubscriberForm(internal_alert_data)
    # The form is valid.
    assert form.is_valid() is True

    # Set the "division" field to have the division_value.
    internal_alert_data["division"] = division_value
    form = InternalAlertsSubscriberForm(internal_alert_data)
    # The form is not valid, becuase the expected_required_field does not have
    # a value.
    assert form.is_valid() is False
    assert {expected_required_field: ["This field is required."]} == form.errors

    # Set the expected_required_field to have a value.
    internal_alert_data[expected_required_field] = valid_required_field_value
    form = InternalAlertsSubscriberForm(internal_alert_data)
    # Now the form is valid.
    assert form.is_valid() is True


def test_form_valid_community_response_form(db, community_response_notification_data):
    """Test putting valid data into the form."""
    form = CommunityResponseSubscriberForm(community_response_notification_data)
    assert form.is_valid()


def test_invalid_phone_number_community_response_form(
    db, community_response_notification_data
):
    """Having invalid data means the form is not valid."""
    # The 'cell_phone' field value is not valid.
    community_response_notification_data["cell_phone"] = "0"

    form = CommunityResponseSubscriberForm(community_response_notification_data)

    assert form.is_valid() is False
    expected_error = (
        "Enter a valid phone number (e.g. (201) 555-0123) or a number "
        "with an international call prefix."
    )
    assert {"cell_phone": [expected_error]} == form.errors


def test_invalid_zip_code_community_response_form(
    db, community_response_notification_data
):
    """Having invalid data means the form is not valid."""
    # The 'zip_code' field value is not valid.
    community_response_notification_data["organization_zip_code"] = "1234"

    form = CommunityResponseSubscriberForm(community_response_notification_data)

    assert form.is_valid() is False
    expected_error = "Either provide a 5 or 9 digit zipcode Ex: 12345 or 12345-1234"
    assert {"organization_zip_code": [expected_error]} == form.errors


def test_form_valid_opioid_overdose_form(db, opioid_overdose_notification_data):
    """Test putting valid data into the form."""
    form = OpioidOverdoseSubscriberForm(opioid_overdose_notification_data)
    assert form.is_valid()


def test_invalid_phone_number_opioid_overdose_form(
    db, opioid_overdose_notification_data
):
    """Having invalid data means the form is not valid."""
    # The 'mobile_phone' field value is not valid.
    opioid_overdose_notification_data["mobile_phone"] = "0"

    form = OpioidOverdoseSubscriberForm(opioid_overdose_notification_data)

    assert form.is_valid() is False
    expected_error = (
        "Enter a valid phone number (e.g. (201) 555-0123) or a number "
        "with an international call prefix."
    )
    assert {"mobile_phone": [expected_error]} == form.errors


def test_form_valid_codered_codeblue_form(db, codered_codeblue_notification_data):
    """Test putting valid data into the form."""
    form = CodeRedCodeBlueSubscriberForm(codered_codeblue_notification_data)
    assert form.is_valid()


def test_invalid_phone_number_codered_codeblue_form(
    db, codered_codeblue_notification_data
):
    """Having invalid data means the form is not valid."""
    # The 'work_phone' field value is not valid.
    codered_codeblue_notification_data["work_phone"] = "0"

    form = CodeRedCodeBlueSubscriberForm(codered_codeblue_notification_data)

    assert form.is_valid() is False
    expected_error = (
        "Enter a valid phone number (e.g. (201) 555-0123) or a number "
        "with an international call prefix."
    )
    assert {"work_phone": [expected_error]} == form.errors


def test_empty_data_codered_codeblue_form(db):
    """Though all CodeRedCodeBlueSubscriberForm fields are optional, at least 1 is required."""
    # Having empty data means the form is not valid.
    form = CodeRedCodeBlueSubscriberForm({})
    assert form.is_valid() is False
    assert {"__all__": ["Please fill in at least 1 field."]} == form.errors

    # Entering at least 1 field makes the form valid.
    form = CodeRedCodeBlueSubscriberForm({"first_name": "Name"})
    assert form.is_valid() is True


def test_form_valid_public_health_preparedness_form(db, php_notification_data):
    """Test putting valid data into the form."""
    form = PublicHealthPreparednessSubscriberForm(php_notification_data)
    assert form.is_valid()


def test_invalid_phone_number_public_health_preparedness_form(
    db, php_notification_data
):
    """Having invalid data means the form is not valid."""
    # The 'cell_phone' field value is not valid.
    php_notification_data["phone_number"] = "0"

    form = PublicHealthPreparednessSubscriberForm(php_notification_data)

    assert form.is_valid() is False
    expected_error = (
        "Enter a valid phone number (e.g. (201) 555-0123) or a number "
        "with an international call prefix."
    )
    assert {"phone_number": [expected_error]} == form.errors


def test_invalid_zip_code_public_health_preparedness_form(db, php_notification_data):
    """Having invalid data means the form is not valid."""
    # The 'zip_code' field value is not valid.
    php_notification_data["organization_zip_code"] = "1234"

    form = PublicHealthPreparednessSubscriberForm(php_notification_data)

    assert form.is_valid() is False
    expected_error = "Either provide a 5 or 9 digit zipcode Ex: 12345 or 12345-1234"
    assert {"organization_zip_code": [expected_error]} == form.errors

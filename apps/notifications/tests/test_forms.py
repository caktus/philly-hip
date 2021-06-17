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

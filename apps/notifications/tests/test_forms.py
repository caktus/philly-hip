from ..forms import InternalAlertsSubscriberForm


def test_asterisks_mark_required_fields(db):
    """Required field names end with an asterisk."""
    form = InternalAlertsSubscriberForm()
    for field_name in form.fields:
        if form.fields[field_name].required:
            assert form.fields[field_name].label.endswith("*") is True
        else:
            assert form.fields[field_name].label.endswith("*") is False


def test_form_valid(db, internal_alert_data):
    """Test putting valid data into the form."""
    form = InternalAlertsSubscriberForm(internal_alert_data)
    assert form.is_valid()


def test_invalid_phone_number(db, internal_alert_data):
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


def test_invalid_zip_code(db, internal_alert_data):
    """Having invalid data means the form is not valid."""
    # The 'zip_code' field value is not valid.
    internal_alert_data["zip_code"] = "1234"

    form = InternalAlertsSubscriberForm(internal_alert_data)

    assert form.is_valid() is False
    expected_error = "Either provide a 5 or 9 digit zipcode Ex: 12345 or 12345-1234"
    assert {"zip_code": [expected_error]} == form.errors

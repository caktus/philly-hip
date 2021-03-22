import pytest

from ..forms import HealthAlertSubscriberForm


@pytest.fixture
def subscribe_data():
    return dict(
        personal_first_name="SpongeBob",
        personal_last_name="SquarePants",
        personal_medical_expertise="Sutures",
        personal_professional_license="1294dk",
        agency_name="The Crabby Patty",
        agency_type="PDPH",
        agency_zip_code="12340",
        agency_work_phone="(201) 555-0123",
        agency_position="Manager",
        network_email="crabbypatty@gmail.com",
        network_fax="(201) 555-0123",
    )


def test_asterisks_mark_required_fields(db):
    form = HealthAlertSubscriberForm()
    for field_name in form.fields:
        if form.fields[field_name].required:
            assert form.fields[field_name].label.endswith("*") is True
        else:
            assert form.fields[field_name].label.endswith("*") is False


def test_form_valid_all_data(db, subscribe_data):
    form = HealthAlertSubscriberForm(subscribe_data)
    assert form.is_valid()


def test_agency_work_phone_optional(db, subscribe_data):
    del subscribe_data["agency_work_phone"]
    form = HealthAlertSubscriberForm(subscribe_data)
    assert form.is_valid()


def test_invalid_phone_number_agency_work_phone(db, subscribe_data):
    subscribe_data["agency_work_phone"] = "23903203"
    form = HealthAlertSubscriberForm(subscribe_data)
    assert form.is_valid() is False
    err = (
        "Enter a valid phone number (e.g. (201) 555-0123) or a number "
        "with an international call prefix."
    )
    assert err in str(form.errors)


def test_invalid_phone_number_network_fax(db, subscribe_data):
    subscribe_data["network_fax"] = "23903203"
    form = HealthAlertSubscriberForm(subscribe_data)
    assert form.is_valid() is False
    err = (
        "Enter a valid phone number (e.g. (201) 555-0123) or a number "
        "with an international call prefix."
    )
    assert err in str(form.errors)


def test_invalid_zip_code(db, subscribe_data):
    subscribe_data["agency_zip_code"] = "23903203"
    form = HealthAlertSubscriberForm(subscribe_data)
    assert form.is_valid() is False
    err = "Either provide a 5 or 9 digit zipcode Ex: 12345 or 12345-1234"
    assert err in str(form.errors)


def test_field_is_required(db, subscribe_data):
    del subscribe_data["personal_first_name"]
    form = HealthAlertSubscriberForm(subscribe_data)
    assert form.is_valid() is False
    err = "This field is required."
    assert err in str(form.errors)

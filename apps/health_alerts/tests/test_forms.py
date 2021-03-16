import pytest

from ..forms import HealthAlertsSignUpForm


@pytest.fixture
def sign_up_data():
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


def test_form_valid_all_data(db, sign_up_data):
    form = HealthAlertsSignUpForm(sign_up_data)
    assert form.is_valid()


def test_agency_work_phone_optional(db, sign_up_data):
    del sign_up_data["agency_work_phone"]
    form = HealthAlertsSignUpForm(sign_up_data)
    assert form.is_valid()


def test_invalid_phone_number_agency_work_phone(db, sign_up_data):
    sign_up_data["agency_work_phone"] = "23903203"
    form = HealthAlertsSignUpForm(sign_up_data)
    assert form.is_valid() is False
    err = (
        "Enter a valid phone number (e.g. (201) 555-0123) or a number "
        "with an international call prefix."
    )
    assert err in str(form.errors)


def test_invalid_phone_number_network_fax(db, sign_up_data):
    sign_up_data["network_fax"] = "23903203"
    form = HealthAlertsSignUpForm(sign_up_data)
    assert form.is_valid() is False
    err = (
        "Enter a valid phone number (e.g. (201) 555-0123) or a number "
        "with an international call prefix."
    )
    assert err in str(form.errors)


def test_invalid_zip_code(db, sign_up_data):
    sign_up_data["agency_zip_code"] = "23903203"
    form = HealthAlertsSignUpForm(sign_up_data)
    assert form.is_valid() is False
    err = "Either provide a 5 or 9 digit zipcode Ex: 12345 or 12345-1234"
    assert err in str(form.errors)


def test_field_is_required(db, sign_up_data):
    del sign_up_data["personal_first_name"]
    form = HealthAlertsSignUpForm(sign_up_data)
    assert form.is_valid() is False
    err = "This field is required."
    assert err in str(form.errors)

from apps.auth_content.forms import ClosedPODContactInformationForm


def test_get_contact_info_form_has_no_user():
    """
    User can only edit their own contact info, so 'user' field is not in the form.
    """
    form = ClosedPODContactInformationForm()
    assert "user" not in form.fields

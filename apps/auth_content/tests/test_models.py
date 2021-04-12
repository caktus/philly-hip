from .factories import (
    ClosedPODChildPageFactory,
    ClosedPODContactInformationFactory,
    ClosedPODHomePageFactory,
)


def test_closedpod_home_page_context_no_children(db, rf):
    """Test 'closedpod_children_pages' context variable when ClosedPODHomePage has no children."""
    closedpod_home_page = ClosedPODHomePageFactory()
    context = closedpod_home_page.get_context(rf.get("/"))
    assert len(context["closedpod_children_pages"]) == 0


def test_closedpod_home_page_context_with_children(db, rf):
    """The context for the ClosedPODHomePage includes its children pages."""
    closedpod_home_page = ClosedPODHomePageFactory()
    child1 = ClosedPODChildPageFactory(parent=closedpod_home_page, title="Child 1")
    child2 = ClosedPODChildPageFactory(parent=closedpod_home_page, title="Child 2")
    expected_results = [child1.page_ptr, child2.page_ptr]

    context = closedpod_home_page.get_context(rf.get("/"))

    assert len(context["closedpod_children_pages"]) == len(expected_results)
    for page in context["closedpod_children_pages"]:
        assert page in expected_results


def test_closedpod_contact_information_string(db):
    """Test the string representation of a ClosedPODContactInformation."""
    contact = ClosedPODContactInformationFactory()
    assert f"ClosedPOD Contact for '{contact.facility_name}'" == str(contact)

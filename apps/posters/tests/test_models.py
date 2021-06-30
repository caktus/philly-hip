from ..models import PosterDetailPage


from .factories import (  # isort: skip
    PosterCategoryFactory,
    PosterDetailPageFactory,
    PosterListPageFactory,
)


def test_posterlistpage_context_no_posters(db, rf):
    """Test the context for a PosterListPage with no children PosterDetailPages."""
    poster_list_page = PosterListPageFactory()
    assert 0 == poster_list_page.get_children().count()

    context = poster_list_page.get_context(rf.get("/someurl/"))
    assert 0 == len(context["posters"])
    assert 0 == len(context["right_nav_headings"])


def test_posterlistpage_context_posters_no_categories(db, rf):
    """Test the context for a PosterListPage with children PosterDetailPages with no categories."""
    poster_list_page = PosterListPageFactory()
    poster1 = PosterDetailPageFactory(parent=poster_list_page, category=None)
    poster2 = PosterDetailPageFactory(parent=poster_list_page, category=None)

    context = poster_list_page.get_context(rf.get("/someurl/"))

    # Posters and categories are in alphabetical order.
    expected_posters = (
        PosterDetailPage.objects.filter(id__in=[poster1.id, poster2.id])
        .order_by("category", "title")
        .live()
    )
    assert list(expected_posters) == list(context["posters"])
    assert ["Other"] == context["right_nav_headings"]


def test_posterlistpage_context_posters_with_and_withoug_categories(db, rf):
    """Test the context for a PosterListPage with children PosterDetailPages with categories."""
    poster_list_page = PosterListPageFactory()
    category_infectioncontrol = PosterCategoryFactory(name="Infection Control")
    category_handwashing = PosterCategoryFactory(name="Handwashing")
    poster_infectioncontrol1 = PosterDetailPageFactory(
        parent=poster_list_page,
        category=category_infectioncontrol,
        title="Infection Control 1",
    )
    poster_handwashing1 = PosterDetailPageFactory(
        parent=poster_list_page, category=category_handwashing, title="Handwashing 1"
    )
    poster_handwashing2 = PosterDetailPageFactory(
        parent=poster_list_page, category=category_handwashing, title="Handwashing 2"
    )
    poster_no_category = PosterDetailPageFactory(
        parent=poster_list_page, category=None, title="Some Poster"
    )

    context = poster_list_page.get_context(rf.get("/someurl/"))

    # Posters and categories are in alphabetical order. The "Other" category is
    # the last category.
    expected_posters = (
        PosterDetailPage.objects.filter(
            id__in=[
                poster_handwashing1.id,
                poster_handwashing2.id,
                poster_infectioncontrol1.id,
                poster_no_category.id,
            ]
        )
        .order_by("category", "title")
        .live()
    )
    assert list(expected_posters) == list(context["posters"])
    assert ["Infection Control", "Handwashing", "Other"] == context[
        "right_nav_headings"
    ]

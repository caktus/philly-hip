from django.urls import reverse

from apps.disease_control.tests.factories import DiseaseControlPageFactory


def test_search_no_query(client, db):
    url = reverse("search")
    response = client.get(url)
    assert response.status_code == 200
    context = response.context
    for key in ["search_query", "search_results", "prev_url"]:
        assert key in response.context


def test_search_with_successful_query(client, db):
    page = DiseaseControlPageFactory(title="foo")
    data = {"query": "foo"}
    url = reverse("search")
    response = client.get(url, data)
    assert response.status_code == 200
    context = response.context
    assert response.context["search_query"] == "foo"
    assert response.context["search_results"].object_list[0].specific == page


def test_search_with_unsuccessful_query(client, db):
    page = DiseaseControlPageFactory(title="foo")
    data = {"query": "bar"}
    url = reverse("search")
    response = client.get(url, data)
    assert response.status_code == 200
    context = response.context
    assert response.context["search_query"] == "bar"
    assert len(response.context["search_results"].object_list) == 0

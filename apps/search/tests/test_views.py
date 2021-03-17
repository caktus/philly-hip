from django.urls import reverse

from apps.common.utils import get_home_page_url
from apps.disease_control.tests.factories import DiseaseControlPageFactory


def test_search_no_query(client, db):
    url = reverse("search")
    response = client.get(url)
    assert response.status_code == 200
    for key in ["search_query", "search_results", "initial_url", "base_params"]:
        assert key in response.context


def test_search_with_successful_query(client, db):
    page = DiseaseControlPageFactory(title="foo")
    data = {"query": "foo"}
    url = reverse("search")
    response = client.get(url, data)
    assert response.status_code == 200
    assert response.context["search_query"] == "foo"
    search_results = response.context["search_results"].object_list
    assert len(search_results) == 1
    assert search_results[0].specific == page


def test_search_with_unsuccessful_query(client, db):
    page = DiseaseControlPageFactory(title="foo")
    data = {"query": "bar"}
    url = reverse("search")
    response = client.get(url, data)
    assert response.status_code == 200
    assert response.context["search_query"] == "bar"
    assert len(response.context["search_results"].object_list) == 0


def test_initial_url_defaults_to_home(client, db):
    url = reverse("search")
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["initial_url"] == get_home_page_url()


def test_initial_url_can_be_provided_in_request(client, db):
    url = reverse("search")
    response = client.get(url, {"initial_url": "/initial"})
    assert response.status_code == 200
    assert response.context["initial_url"] == "/initial"

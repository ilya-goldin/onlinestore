import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED,\
    HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from products.models import Product


@pytest.mark.django_db
def test_retrieve_product(api_client, products):
    prod = products(qty=5)[1]
    url = reverse('products-detail', args=(prod.id,))

    resp = api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == HTTP_200_OK
    assert resp_json.get('name') == prod.name
    assert resp_json.get('description') == prod.description
    assert resp_json.get('price') == prod.price


@pytest.mark.django_db
def test_list_products(api_client, products):
    prods = products(qty=10)
    url = reverse('products-list')

    resp = api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == HTTP_200_OK
    assert len(resp_json) == 10
    for i in range(10):
        assert resp_json[i].get('name') == prods[i].name
        assert resp_json[i].get('price') == prods[i].price
        assert resp_json[i].get('description') == prods[i].description


@pytest.mark.django_db
def test_user_create_products(api_client):
    url = reverse('products-list')

    resp = api_client.post(url, {
        'name': 'Name 1',
        'description': 'Description 1',
        'price': 1
    })

    assert resp.status_code == HTTP_403_FORBIDDEN
    assert Product.objects.all().count() == 0


@pytest.mark.django_db
def test_admin_create_products(api_client_admin):
    url = reverse('products-list')

    resp = api_client_admin.post(url, {
        'name': 'Name 1',
        'description': 'Description 1',
        'price': 1
    })

    assert resp.status_code == HTTP_201_CREATED
    assert Product.objects.all().count() == 1


@pytest.mark.django_db
def test_user_update_products(api_client, products):
    prods = products()[0]
    url = reverse('products-detail', args=(prods.id,))

    resp = api_client.patch(url, {
        'name': 'Name 1',
        'description': 'Description 1',
        'price': 1
    }, )

    assert resp.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_update_products(api_client_admin, products):
    prods = products()[0]
    url = reverse('products-detail', args=(prods.id,))

    resp = api_client_admin.patch(url, {
        'name': 'Name 1',
        'description': 'Description 1',
        'price': 1
    }, )

    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_user_destroy_products(api_client, products):
    prods = products()[0]
    url = reverse('products-detail', args=(prods.id,))

    resp = api_client.delete(url)

    assert resp.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_destroy_products(api_client_admin, products):
    prods = products()[0]
    url = reverse('products-detail', args=(prods.id,))

    resp = api_client_admin.delete(url)

    assert resp.status_code == HTTP_204_NO_CONTENT
    assert Product.objects.all().count() == 0


@pytest.mark.django_db
def test_price_filter_products(api_client, products):
    products(qty=5)
    url = reverse('products-list')

    resp_max = api_client.get(url, {'price_max': 100})
    resp_min = api_client.get(url, {'price_min': 100})

    assert resp_max.status_code == HTTP_200_OK
    resp_json = resp_max.json()
    assert len(resp_json) == 0
    resp_json = resp_min.json()
    assert len(resp_json) != 0


@pytest.mark.django_db
def test_name_filter_products(api_client, products):
    prods = products(qty=5)[0]
    url = reverse('products-list')

    resp = api_client.get(url, {'name__contains': prods.name[0:10]})
    resp_json = resp.json()[0]

    assert resp.status_code == HTTP_200_OK
    assert resp_json.get('name') == prods.name
    assert resp_json.get('description') == prods.description
    assert resp_json.get('price') == prods.price


@pytest.mark.django_db
def test_description_filter_products(api_client, products):
    prods = products(qty=5)[0]
    url = reverse('products-list')

    resp = api_client.get(url, {'description__contains': prods.description[0:50]})
    resp_json = resp.json()[0]

    assert resp.status_code == HTTP_200_OK
    assert resp_json.get('name') == prods.name
    assert resp_json.get('description') == prods.description
    assert resp_json.get('price') == prods.price

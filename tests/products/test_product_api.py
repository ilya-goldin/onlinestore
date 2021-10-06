import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, \
    HTTP_405_METHOD_NOT_ALLOWED
from products.models import Product


@pytest.mark.django_db
def test_first_product(api_client, products):
    prod = products(qty=10)[4]
    url = reverse('products-detail', args=(prod.id,))

    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json.get('name') == prod.name
    assert resp_json.get('description') == prod.description
    assert resp_json.get('price') == prod.price


@pytest.mark.django_db
def test_list_products(api_client, products):
    prods = products(qty=20)
    url = reverse('products-list')

    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == 20
    for i in range(20):
        assert resp_json[i].get('name') == prods[i].name
        assert resp_json[i].get('price') == prods[i].price
        assert resp_json[i].get('description') == prods[i].description


@pytest.mark.django_db
def test_price_filter_products(api_client, products):
    prods = products(qty=5)
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
    prods = products(qty=5)
    url = reverse('products-list')

    resp = api_client.get(url, {'name__contains': prods[0].name[0:10]})

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()[0]
    assert resp_json.get('name') == prods[0].name
    assert resp_json.get('description') == prods[0].description
    assert resp_json.get('price') == prods[0].price


@pytest.mark.django_db
def test_description_filter_products(api_client, products):
    prods = products(qty=5)
    url = reverse('products-list')

    resp = api_client.get(url, {'description__contains': prods[0].description[0:50]})

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()[0]
    assert resp_json.get('name') == prods[0].name
    assert resp_json.get('description') == prods[0].description
    assert resp_json.get('price') == prods[0].price


@pytest.mark.django_db
def test_user_create_products(api_client, products):
    prods = products()
    url = reverse('products-list')

    resp = api_client.post(url, {
        'name': 'Name 1',
        'description': 'Description 1',
        'price': 1
    })

    assert resp.status_code == HTTP_403_FORBIDDEN
    q = Product.objects.all()
    assert q.count() == 1


@pytest.mark.django_db
def test_user_update_products(api_client, products):
    prods = products()[0]
    url = reverse('products-detail', args=(prods.id,))

    resp = api_client.post(url, {
        'name': 'Name 1',
        'description': 'Description 1',
        'price': 1
    }, )

    assert resp.status_code == HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_user_destroy_products(api_client, products):
    prods = products()[0]
    url = reverse('products-detail', args=(prods.id,))

    resp = api_client.post(url)

    assert resp.status_code == HTTP_405_METHOD_NOT_ALLOWED

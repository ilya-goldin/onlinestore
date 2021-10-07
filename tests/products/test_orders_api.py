from random import randint
from datetime import date
import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED,\
    HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from products.models import Order, Product
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_retrieve_user_order(api_client, orders):
    user = User.objects.get(username='lauren')
    order = orders(qty=5)[3]
    user_order = orders(user=user)[0]
    url = reverse('orders-detail', args=(order.id,))
    user_url = reverse('orders-detail', args=(user_order.id,))

    resp = api_client.get(url)
    user_resp = api_client.get(user_url)

    assert resp.status_code == HTTP_404_NOT_FOUND
    assert user_resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_admin_order(api_client_admin, orders):
    order = orders()[0]
    url = reverse('orders-detail', args=(order.id,))

    resp = api_client_admin.get(url)

    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_user_list_order(api_client, orders):
    user = User.objects.get(username='lauren')
    order = orders(qty=5)
    user_order = orders(qty=5, user=user)[0]
    url = reverse('orders-list')

    resp = api_client.get(url)
    resp_json = resp.json()

    assert resp.status_code == HTTP_200_OK
    assert len(resp_json) == 5


@pytest.mark.django_db
def test_admin_list_order(api_client_admin, orders):
    order = orders(qty=10)
    url = reverse('orders-list')

    resp = api_client_admin.get(url)
    resp_json = resp.json()

    assert resp.status_code == HTTP_200_OK
    assert len(resp_json) == 10


@pytest.mark.django_db
def test_create_order(api_client, products):
    products_set = products(qty=5)
    qty = randint(1, 10)
    product = [{'product': i.id, 'qty': qty} for i in products_set]
    url = reverse('orders-list')
    order_value = sum(Product.objects.all().values_list('price', flat=True)) * qty

    resp = api_client.post(url, {
        'product': product,
    }, format='json')
    resp_json = resp.json()

    assert resp.status_code == HTTP_201_CREATED
    assert Order.objects.all().count() == 1
    assert order_value == resp_json.get('order_value')


@pytest.mark.django_db
def test_update_order(api_client, products, orders):
    order = orders(user=User.objects.get(username='lauren'))[0]
    qty = randint(1, 10)
    product = [{'product': i.id, 'qty': qty} for i in products(qty=10)]
    order_value = sum(Product.objects.all().values_list('price', flat=True)) * qty
    url = reverse('orders-detail', args=(order.id,))

    resp = api_client.patch(url, {
        'product': product,
    }, format='json')
    resp_status = api_client.patch(url, {
        'product': product,
        'status': 'DONE',
    }, format='json')
    resp_json = resp.json()

    assert resp.status_code == HTTP_200_OK
    assert resp_status.status_code == HTTP_400_BAD_REQUEST
    assert Order.objects.all().count() == 1
    assert order_value == resp_json.get('order_value')


@pytest.mark.django_db
def test_destroy_order(api_client, orders):
    order = orders()[0]
    url = reverse('orders-detail', args=(order.id,))

    resp = api_client.delete(url)

    assert resp.status_code == HTTP_403_FORBIDDEN
    assert Order.objects.all().count() == 1


@pytest.mark.django_db
def test_admin_destroy_order(api_client_admin, orders):
    order = orders()[0]
    url = reverse('orders-detail', args=(order.id,))

    resp = api_client_admin.delete(url)

    assert resp.status_code == HTTP_204_NO_CONTENT
    assert Order.objects.all().count() == 0


@pytest.mark.django_db
def test_status_filter_order(api_client, orders):
    user = User.objects.get(username='lauren')
    orders(qty=2, user=user, status='DONE')
    orders(qty=1, user=user, status='NEW')
    orders(qty=1, user=user, status='IN_PROGRESS')
    url = reverse('orders-list')

    resp_1 = api_client.get(url, {
        'status': 'DONE',
    })
    resp_2 = api_client.get(url, {
        'status': 'NEW',
    })
    resp_3 = api_client.get(url, {
        'status': 'IN_PROGRESS',
    })

    assert resp_1.status_code == HTTP_200_OK
    resp_json = resp_1.json()
    assert len(resp_json) == 2
    assert resp_2.status_code == HTTP_200_OK
    resp_json = resp_2.json()
    assert len(resp_json) == 1
    assert resp_3.status_code == HTTP_200_OK
    resp_json = resp_3.json()
    assert len(resp_json) == 1


@pytest.mark.django_db
def test_value_filter_order(api_client, orders):
    user = User.objects.get(username='lauren')
    order_value = randint(100, 1000)
    orders(user=user, order_value=order_value)
    orders(user=user, order_value=order_value + 500)
    url = reverse('orders-list')

    resp_1 = api_client.get(url, {
        'order_value_max': order_value,
    })
    resp_2 = api_client.get(url, {
        'order_value_min': order_value,
    })
    resp_json = resp_1.json()

    assert resp_1.status_code == HTTP_200_OK
    assert len(resp_json) == 1
    assert resp_2.status_code == HTTP_200_OK
    resp_json = resp_2.json()
    assert len(resp_json) == 2


@pytest.mark.django_db
def test_created_at_filter_order(api_client, orders):
    user = User.objects.get(username='lauren')
    orders(qty=2, user=user)
    url = reverse('orders-list')

    after = api_client.get(url, {
        'created_at_after': date.today().strftime('%Y-%m-%d')
    })
    before = api_client.get(url, {
        'created_at_before': date.today().strftime('%Y-%m-%d')
    })
    after_json = after.json()
    before_json = before.json()

    assert after.status_code == HTTP_200_OK
    assert len(after_json) == 2
    assert before.status_code == HTTP_200_OK
    assert len(before_json) == 0


@pytest.mark.django_db
def test_updated_at_filter_order(api_client, orders):
    user = User.objects.get(username='lauren')
    orders(qty=2, user=user)
    url = reverse('orders-list')

    after = api_client.get(url, {
        'updated_at_after': date.today().strftime('%Y-%m-%d')
    })
    before = api_client.get(url, {
        'updated_at_before': date.today().strftime('%Y-%m-%d')
    })
    after_json = after.json()
    before_json = before.json()

    assert after.status_code == HTTP_200_OK
    assert len(after_json) == 2
    assert before.status_code == HTTP_200_OK
    assert len(before_json) == 0



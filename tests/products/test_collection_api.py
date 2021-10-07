import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED,\
    HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from products.models import Review
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_first_collection(api_client, collections):
    collection = collections(qty=5)[3]
    url = reverse('product-collections-detail', args=(collection.id,))

    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json.get('title') == collection.title
    assert resp_json.get('note') == collection.note


@pytest.mark.django_db
def test_list_collection(api_client, collections):
    collection = collections(qty=20)
    url = reverse('product-collections-list')

    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == 20
    for i in range(20):
        assert resp_json[i].get('title') == collection[i].title
        assert resp_json[i].get('note') == collection[i].note


@pytest.mark.django_db
def test_admin_create_collection(api_client, collections, products):
    user = User.objects.create(username='admin_user', password='admin_password', is_staff=True)
    api_client.force_authenticate(user=user)
    products = [i.id for i in products(qty=5)][1:3]
    url = reverse('product-collections-list')

    resp = api_client.post(url, {
        'title': 'Title',
        'note': 'Description',
        'items': products
    })

    assert resp.status_code == HTTP_201_CREATED
    assert Review.objects.all().count() == 0


@pytest.mark.django_db
def test_user_create_collection(api_client, collections):
    user = User.objects.create(username='lauren2', password='123secret123',)
    api_client.force_authenticate(user=user)
    url = reverse('product-collections-list')

    resp = api_client.post(url, {
        'title': 'Title',
        'note': 'Description',
        'items': 1
    })

    assert resp.status_code == HTTP_403_FORBIDDEN
    assert Review.objects.all().count() == 0


@pytest.mark.django_db
def test_admin_update_collection(api_client, collections, products):
    user = User.objects.create(username='admin_user', password='admin_password', is_staff=True)
    api_client.force_authenticate(user=user)
    products = products(qty=5)[1:3]
    collection = collections(items=products)[0]
    url = reverse('product-collections-detail', args=(collection.id,))

    resp = api_client.patch(url, {
        'title': 'New title',
        'note': 'New description',
    })

    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_user_update_collection(api_client, collections, products):
    user = User.objects.create(username='lauren2', password='123secret123',)
    api_client.force_authenticate(user=user)
    products = products(qty=5)[1:3]
    collection = collections(items=products)[0]
    url = reverse('product-collections-detail', args=(collection.id,))

    resp = api_client.patch(url, {
        'title': 'New title',
        'note': 'New description',
    })

    assert resp.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_destroy_collection(api_client, collections):
    user = User.objects.create(username='admin_user', password='admin_password', is_staff=True)
    api_client.force_authenticate(user=user)
    collection = collections()[0]
    url = reverse('product-collections-detail', args=(collection.id,))

    resp = api_client.delete(url)

    assert resp.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_destroy_collection(api_client, collections):
    user = User.objects.create(username='lauren3', password='123secret123')
    api_client.force_authenticate(user=user)
    collection = collections()[0]
    url = reverse('product-collections-detail', args=(collection.id,))

    resp = api_client.delete(url)

    assert resp.status_code == HTTP_403_FORBIDDEN

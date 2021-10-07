import pytest
from datetime import datetime as dt
from random import randint
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED,\
    HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from products.models import Review, Product
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_first_review(api_client, reviews):
    review = reviews(qty=30)[3]
    url = reverse('product-reviews-detail', args=(review.id,))

    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json.get('user').get('username') == review.user.username
    assert resp_json.get('product_id') == review.product.id
    assert resp_json.get('review_text') == review.review_text
    assert resp_json.get('score') == review.score


@pytest.mark.django_db
def test_list_review(api_client, reviews):
    review = reviews(qty=20)
    url = reverse('product-reviews-list')

    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == 20
    for i in range(20):
        assert resp_json[i].get('user').get('username') == review[i].user.username
        assert resp_json[i].get('product_id') == review[i].product.id
        assert resp_json[i].get('review_text') == review[i].review_text
        assert resp_json[i].get('score') == review[i].score


@pytest.mark.django_db
def test_user_id_filter_review(api_client, reviews):
    review = reviews(qty=20)
    url = reverse('product-reviews-list')

    user_id = User.objects.first().id
    resp = api_client.get(url, {'user': user_id})

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    for i in resp_json:
        assert i.get('user').get('id') == user_id


@pytest.mark.django_db
def test_product_id_filter_review(api_client):
    url = reverse('product-reviews-list')

    product_id = randint(1, 50)
    resp = api_client.get(url, {'product_id': product_id})

    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    for i in resp_json:
        assert i.get('user').get('id') == product_id


@pytest.mark.django_db
def test_date_filter_review(api_client, reviews):
    review = reviews(qty=20)
    url = reverse('product-reviews-list')

    created_at_after = api_client.get(url, {
        'created_at_after': dt.now().strftime('%Y-%m-%dT%H:%M')
    })
    created_at_before = api_client.get(url, {
        'created_at_before': dt.now().strftime('%Y-%m-%dT%H:%M')
    })

    assert created_at_after.status_code == HTTP_200_OK
    resp_json = created_at_after.json()
    assert len(resp_json) == 20
    assert created_at_before.status_code == HTTP_200_OK
    resp_json = created_at_before.json()
    assert len(resp_json) == 0


@pytest.mark.django_db
def test_user_create_review(api_client, products):
    user = User.objects.create(username='lauren2', password='123secret123')
    api_client.force_authenticate(user=user)
    url = reverse('product-reviews-list')
    prod_1 = products()[0].id
    prod_2 = products()[0].id
    prod = Product.objects.first().id

    resp_1 = api_client.post(url, {
        'product_id': prod_1,
        'review_text': 'Description 1',
        'score': 1
    })
    resp_2 = api_client.post(url, {
        'product_id': prod,
        'review_text': 'Description 2',
        'score': 2
    })
    resp_3 = api_client.post(url, {
        'product_id': prod_2,
        'review_text': 'Description 2',
        'score': 2
    })

    assert resp_1.status_code == HTTP_201_CREATED
    assert resp_2.status_code == HTTP_400_BAD_REQUEST
    assert resp_3.status_code == HTTP_201_CREATED
    assert Review.objects.all().count() == 2


@pytest.mark.django_db
def test_user_update_review(api_client, products, reviews):
    user = User.objects.create(username='lauren3', password='123secret123')
    api_client.force_authenticate(user=user)
    review_1 = reviews(user=user)[0]
    review_2 = reviews()[0]
    url_1 = reverse('product-reviews-detail', args=(review_1.id,))
    url_2 = reverse('product-reviews-detail', args=(review_2.id,))

    resp_1 = api_client.patch(url_1, {
        'review_text': 'New description',
        'score': 1
    })
    resp_2 = api_client.patch(url_2, {
        'review_text': 'New description',
        'score': 1
    })

    assert resp_1.status_code == HTTP_200_OK
    assert resp_2.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_destroy_review(api_client, products, reviews):
    user = User.objects.create(username='lauren3', password='123secret123')
    api_client.force_authenticate(user=user)
    review_1 = reviews(user=user)[0]
    review_2 = reviews()[0]
    url_1 = reverse('product-reviews-detail', args=(review_1.id,))
    url_2 = reverse('product-reviews-detail', args=(review_2.id,))

    resp_1 = api_client.delete(url_1)
    resp_2 = api_client.patch(url_2)

    assert resp_1.status_code == HTTP_204_NO_CONTENT
    assert resp_2.status_code == HTTP_403_FORBIDDEN

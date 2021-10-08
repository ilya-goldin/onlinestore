import pytest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker
from faker import Faker
from random import randint
from products.models import Product, Collection, Review, Order

fake = Faker()
Faker.seed(1)


@pytest.fixture
def api_client():
    """Фикстура для клиента API"""

    token = 'a36d1de423bd0f7c9028428754d889ecd1613f4f'
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    user = User.objects.create(username='lauren')
    user.password = make_password('123_secret_123')
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def api_client_admin():
    """Фикстура для admin API"""

    client = APIClient()
    user = User.objects.create(username='admin_user', password='admin_password', is_staff=True)
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def products():
    """Фикстура для Product"""

    def func(qty=1):
        Faker.seed(randint(0, 500))
        out = []
        for _ in range(qty):
            out.append(baker.make(
                Product,
                description=fake.text(),
                price=fake.pyint(min_value=100, max_value=10000),
            ))
        return out
    return func


@pytest.fixture
def reviews():
    """Фикстура для Review"""

    def func(qty=1, **kwargs):
        Faker.seed(randint(0, 500))
        out = []
        for _ in range(qty):
            out.append(baker.make(
                Review,
                review_text=fake.text(),
                score=fake.pyint(min_value=1, max_value=5),
                **kwargs,
            ))
        return out
    return func


@pytest.fixture
def collections():
    """Фикстура для Collection"""

    def func(qty=1, **kwargs):
        return baker.make(
            Collection,
            _quantity=qty,
            **kwargs,
        )
    return func


@pytest.fixture
def orders():
    """Фикстура для Order"""

    def func(qty=1, **kwargs):
        return baker.make(
            Order,
            _quantity=qty,
            **kwargs,
        )
    return func

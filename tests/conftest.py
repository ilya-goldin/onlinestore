import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from faker import Faker
from products.models import Product, Collection, Review, Order

fake = Faker()
Faker.seed(1)


@pytest.fixture
def api_client():
    """Фикстура для клиента API"""

    token = 'a36d1de423bd0f7c9028428754d889ecd1613f4f'
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    return client


@pytest.fixture
def products():
    """Фикстура для Product"""

    def func(qty=1):
        out = []
        for _ in range(qty):
            out.append(baker.make(
                Product,
                name=fake.word(),
                description=fake.text(),
                price=fake.pyint(min_value=100, max_value=10000),
            ))
        return out
    return func


@pytest.fixture
def reviews():
    """Фикстура для Review"""

    def func(qty=1):
        out = []
        for _ in range(qty):
            out.append(baker.make(
                Review,
                review_text=fake.text(),
                score=fake.pyint(min_value=1, max_value=5),
            ))
        return out
    return func


@pytest.fixture
def collections():
    """Фикстура для Collection"""

    def func(qty=1):
        return baker.make(Collection, _quantity=qty)
    return func

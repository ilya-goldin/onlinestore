import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from products.models import Product, Collection, Review, Order, OrderProducts


@pytest.fixture
def api_client():
    """Фикстура для клиента API."""

    return APIClient()


@pytest.fixture
def products():
    """Фикстура для Product"""

    def func(qty=1):
        return baker.make(Product, _quantity=qty)
    return func


@pytest.fixture
def collections():
    """Фикстура для Collection"""

    def func(qty=1):
        return baker.make(Collection, _quantity=qty)
    return func

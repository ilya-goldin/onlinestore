import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.status import HTTP_201_CREATED


@pytest.mark.django_db
def test_user_token(api_client):
    user = User.objects.get(username='lauren')
    url = reverse('token-list')

    resp = api_client.get(url, {
        'username': user.username,
        'password': '123_secret_123',
    })

    # assert resp.status_code == HTTP_201_CREATED
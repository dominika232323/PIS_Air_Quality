import pytest
from django.urls import reverse

def test_welcome_user(client):
    response = client.get(reverse('welcome_page'))
    assert response.status_code == 200
    assert "Welcome! To see all stations, use /all. To see specific station info use /<station_id>" in response.content.decode()


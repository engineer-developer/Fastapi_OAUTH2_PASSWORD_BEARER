import pytest
from httpx import AsyncClient


@pytest.fixture
async def auth_data():
    return {
        "grant_type": "password",
        "username": "user@example.com",
        "password": "1234567890",
    }


@pytest.fixture
async def login(async_client: AsyncClient, auth_data):
    auth_url = "/token"
    auth_headers = {"Content-type": "application/x-www-form-urlencoded"}
    auth_response = await async_client.post(
        auth_url, data=auth_data, headers=auth_headers
    )
    assert auth_response.status_code == 200


@pytest.fixture
async def new_user():
    return {
        "username": "Bob",
        "email": "bob@example.com",
        "role": "client",
        "password": "0987654321",
    }

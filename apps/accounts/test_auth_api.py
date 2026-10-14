import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

REGISTER = "/api/v1/auth/register/"
LOGIN = "/api/v1/auth/login/"
REFRESH = "/api/v1/auth/refresh/"
LOGOUT = "/api/v1/auth/logout/"
PASSWORD = "StrongPass123!"


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_register_returns_user_and_tokens(client):
    r = client.post(
        REGISTER,
        {"email": "Anna@Example.com", "password": PASSWORD, "first_name": "Анна"},
        format="json",
    )
    assert r.status_code == 201
    assert r.data["user"]["email"] == "anna@example.com"
    assert r.data["access"] and r.data["refresh"]
    assert User.objects.filter(email="anna@example.com").exists()


@pytest.mark.django_db
def test_register_duplicate_email_is_rejected_case_insensitive(client):
    User.objects.create_user("a@example.com", PASSWORD)
    r = client.post(REGISTER, {"email": "A@Example.com", "password": PASSWORD}, format="json")
    assert r.status_code == 400
    assert "email" in r.data


@pytest.mark.django_db
def test_register_weak_password_is_rejected(client):
    r = client.post(REGISTER, {"email": "b@example.com", "password": "123"}, format="json")
    assert r.status_code == 400
    assert "password" in r.data


@pytest.mark.django_db
def test_login_ok_is_case_insensitive(client):
    User.objects.create_user("a@example.com", PASSWORD)
    r = client.post(LOGIN, {"email": "A@Example.com", "password": PASSWORD}, format="json")
    assert r.status_code == 200
    assert r.data["access"] and r.data["refresh"]
    assert r.data["user"]["email"] == "a@example.com"


@pytest.mark.django_db
def test_login_wrong_password(client):
    User.objects.create_user("a@example.com", PASSWORD)
    r = client.post(LOGIN, {"email": "a@example.com", "password": "wrong"}, format="json")
    assert r.status_code == 401


@pytest.mark.django_db
def test_refresh_rotates_and_logout_blacklists(client):
    User.objects.create_user("a@example.com", PASSWORD)
    login = client.post(LOGIN, {"email": "a@example.com", "password": PASSWORD}, format="json")

    refreshed = client.post(REFRESH, {"refresh": login.data["refresh"]}, format="json")
    assert refreshed.status_code == 200
    assert refreshed.data["access"]
    new_refresh = refreshed.data["refresh"]

    # старый refresh после обновления больше не работает
    old = client.post(REFRESH, {"refresh": login.data["refresh"]}, format="json")
    assert old.status_code == 401

    assert client.post(LOGOUT, {"refresh": new_refresh}, format="json").status_code == 200
    after = client.post(REFRESH, {"refresh": new_refresh}, format="json")
    assert after.status_code == 401

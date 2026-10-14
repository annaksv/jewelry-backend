import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user_normalizes_email():
    user = User.objects.create_user(email="Test@Example.COM", password="pass12345")
    assert user.email == "test@example.com"
    assert user.check_password("pass12345")
    assert not user.is_staff


@pytest.mark.django_db
def test_create_superuser():
    admin = User.objects.create_superuser(email="admin@example.com", password="pass12345")
    assert admin.is_staff and admin.is_superuser


@pytest.mark.django_db
def test_email_is_unique():
    User.objects.create_user(email="a@example.com", password="pass12345")
    with pytest.raises(Exception):
        User.objects.create_user(email="a@example.com", password="other12345")

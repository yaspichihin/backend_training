import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("kot@pes.com", "password", 200),  # Успешная первичной регистрации
        ("kot@pes.com", "password", 409),  # Отказ поатороной регистрации
        ("not_email", "password", 422),  # Отказ неакерная валидация
    ],
)
async def test_register_user(email, password, status_code, async_client: AsyncClient):
    response = await async_client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test@test.com", "test", 200),  # Успешная аутентификация
        ("test@test.com", "wrong_password", 401),  # Ошибочный пароль
        ("not_exists@example.com", "password", 401),  # Несуществующий пользователь
    ],
)
async def test_login_user(email, password, status_code, async_client: AsyncClient):
    response = await async_client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code

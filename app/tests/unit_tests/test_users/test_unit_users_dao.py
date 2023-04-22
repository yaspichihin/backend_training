import pytest

from app.users.dao import UsersDAO


@pytest.mark.parametrize("user_id,email,exsists",
    [
        (1, "test@test.com", True),  # Проверка существующего пользователя
        (2, "artem@example.com", True),  # Проверка существующего пользователя
        (4, "not_exists_user@example.com", False),  # Проверка не существующего пользователя
    ])
async def test_user_find_by_id(user_id, email, exsists):
    user = await UsersDAO.select_one_or_none_filter_by(id=user_id)
    if exsists:
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user

from datetime import datetime
from fastapi import Depends, Request
from jose import jwt, JWTError

from app.config import settings

from app.users.dao import UsersDAO

from app.users.models import Users

from app.exceptions import (
    IncorrcetTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException)


# Получение данных, которые должны храниться в токене клиента
def get_token(
    request: Request,
) -> str:
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token

# Определение какой именно пользователь перед нами
async def get_current_user(
    token: str = Depends(get_token),
) -> Users:
    # Попытка декодировать токен
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            settings.jwt_algorithm)
    except JWTError:
        raise IncorrcetTokenFormatException
    # Проверим срок действия токена
    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException
    # Проверим срвпадение токена и пользователя
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    # Проверим наличие пользователя в DB
    user = await UsersDAO.select_one_or_none_filter_by(id = int(user_id))
    if not user:
        raise UserIsNotPresentException
    # Возращаем модель пользователя
    return user

# Определение является ли пользователь админом
async def get_current_admin_user(
    current_user: Users = Depends(get_current_user),
) -> Users:
    # Т.к. Админов пока нет, пускай каждый пользователь админ
    # if current_user.role != "Administrator":
    #     raise UserIsNotAdminException
    return current_user
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.users.dao import UsersDAO
from app.users.models import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.jwt_secret_key, settings.jwt_algorithm)
    return encode_jwt


async def authenticate_user(
    email: EmailStr,
    password: str,
) -> Users:
    # Проверим наличие пользователя
    user = await UsersDAO.select_one_or_none_filter_by(email=email)
    # Вернуть None если пользователь не обнаружен или пароль не совпадает
    if user and verify_password(password, user.hashed_password):
        return user

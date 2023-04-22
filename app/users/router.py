from fastapi import APIRouter, Depends, Response

from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException

from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dependencies import get_current_admin_user, get_current_user

from app.users.dao import UsersDAO

from app.users.models import Users

from app.users.schemas import SAuth, SUsers


router_auth = APIRouter(
    prefix = "/auth",
    tags = ["Auth"]
)

router_user = APIRouter(
    prefix = "/user",
    tags = ["Users"]
)

# router_auth

@router_auth.post("/register")
async def register_user(
    user_data: SAuth,
) -> str:
    # Если пользователь с такой почтой существует вернуть ошибку
    if await UsersDAO.select_all_filter_by(email=user_data.email):
        raise UserAlreadyExistsException
    # Захешировать пароль
    hashed_password = get_password_hash(user_data.password)
    # Добавить хэш пароля в базу
    await UsersDAO.add_rows(email=user_data.email, hashed_password=hashed_password)
    return "Успешная регистрация"

@router_auth.post("/login")
async def login_user(
    response: Response,
    user_data: SAuth,
) -> str:
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return "Успешный вход"

@router_auth.post("/logout")
async def logout_user(
    response: Response,
) -> str:
    # Добавляем Response для удаления куки
    response.delete_cookie("booking_access_token")
    return "Успешный выход"


# router_user

@router_user.get("/me")
async def get_me(
    current_user: Users = Depends(get_current_user),
) -> SUsers:
    return current_user

@router_user.get("/all")
async def get_all_users(
    current_user: Users = Depends(get_current_admin_user),
) -> list[SUsers]:
    return await UsersDAO.select_all_filter()
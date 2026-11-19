from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.core.config import settings
from backend.dependencies import (
    AdminDep,
    AuthServiceDep,
    CurrentUserDep,
    UserServiceDep,
)
from backend.schemas import Token, UserCreateSchema, UserOutSchema

router = APIRouter(prefix=settings.api.auth, tags=["auth"])


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServiceDep,
) -> Token:
    return await auth_service.login(form_data.username, form_data.password)


@router.post("/register", response_model=UserOutSchema)
async def get_register_user(
    data: UserCreateSchema,
    user_service: UserServiceDep,
    admin: AdminDep,
):
    return await user_service.create_user(data)


@router.get("/me", response_model=UserOutSchema)
async def get_me(user: CurrentUserDep):
    return user


@router.post("/logout")
async def logout(refresh_token: str, auth_service: AuthServiceDep):
    auth_service.logout(refresh_token)
    return {"message": "logout successful"}


@router.get("/getusers", response_model=list[UserOutSchema])
async def get_users_all(user_service: UserServiceDep):
    return await user_service.get_all()

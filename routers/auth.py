from typing import Annotated
from datetime import timedelta
from auth_config import (
    SECRET_KEY, ALGORITHM,
    create_refresh_token, ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS, create_access_token
)
from role import get_current_user, require_role
from auth_config import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from orm import AsyncORM
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UserCreateSchema, UserOutSchema, Token
from database import SessionDep
from models import UserRole
from fastapi.security import OAuth2PasswordRequestForm

revoked_refresh_tokens: set[str] = set()

router =APIRouter(prefix="/oauth", tags=["auth"])

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    user = await AsyncORM.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.user_name, "type": "access"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": user.user_name},
        expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserOutSchema)
async def get_register_user(
        data: UserCreateSchema,
        session: SessionDep,
        admin = Depends(require_role(UserRole.admin)),
):
    user = await AsyncORM.create_user(session, data)
    return {
        "user_id": user.user_id,
        "user_name": user.user_name,
        "role": user.role
    }

@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    return {
        "user_id": user.user_id,
        "user_name": user.user_name,
        "role": user.role
    }

@router.post("/logout")
async def logout(refresh_token: str):
    revoked_refresh_tokens.add(refresh_token)
    return {"message": "logout successful",}
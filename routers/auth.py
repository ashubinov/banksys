from authx import TokenResponse
from auth_config import security
from orm import AsyncORM
from fastapi import APIRouter, Response, Depends, HTTPException
from schemas import UserCreateSchema, UserOutSchema, LoginRequestSchema
from database import SessionDep
from models import UserRole
from role import require_role
router =APIRouter(prefix="/auth", tags=["auth"])

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

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequestSchema, response: Response,  session: SessionDep):
    user = await AsyncORM.authenticate_user(session, data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = security.create_access_token(uid = str(user.user_id))
    refresh_token = security.create_refresh_token(uid = str(user.user_id))

    security.set_access_cookies(access_token, response)
    security.set_refresh_cookies(refresh_token, response)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.get("/me")
async def get_me(session: SessionDep, token = Depends(security.access_token_required)):
    user_id = int(token.sub)

    user = await AsyncORM.get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.user_id,
        "user_name": user.user_name,
        "role": user.role
    }

@router.get("/logout")
async def logout(response: Response):
    security.unset_access_cookies(response)
    security.unset_refresh_cookies(response)
    return {"message": "logout successful"}
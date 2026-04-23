from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database import SessionDep
from orm import AsyncORM
from models import UserORM, UserRole
from auth_config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="oauth/token")

async def get_current_user(
        session: SessionDep,
        token: Annotated[str, Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type")
        if username is None or token_type != "access":
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user = await AsyncORM.get_user_by_username(session, username=username)
    if user is None:
        raise credentials_exception
    return user

def require_role(*allowed_roles: UserRole | str):
    async def role_checker(current_user: Annotated[UserORM, Depends(get_current_user)]) -> UserORM:
        normalized_role = {role.value if isinstance(role, UserRole) else role for role in allowed_roles}
        if current_user.role not in normalized_role:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user
    return role_checker
from auth_config import security
from orm import AsyncORM
from fastapi import Depends, HTTPException
from database import SessionDep
from models import UserORM, UserRole


def require_role(*allowed_roles: UserRole | str):
    async def role_checker(
            session: SessionDep,
            token: str = Depends(security.access_token_required),
    ) -> UserORM:
        user_id = int(token.sub)
        user = await AsyncORM.get_user_by_id(session, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        normalized_role = {role.value if isinstance(role, UserRole) else role for role in allowed_roles}
        if user.role not in normalized_role:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    return role_checker
from backend.core.exceptions import AuthenticationError
from backend.core.utils.auth_utils import create_access_token, create_refresh_token
from backend.core.utils.password import verify_password
from backend.repositories.user import UserRepository
from backend.schemas.user import Token

# хранилище отозванных refresh-токенов (в памяти процесса)
revoked_refresh_tokens: set[str] = set()


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repo = repository

    async def login(self, username: str, password: str) -> Token:
        user = await self.repo.get_by_username(username)
        if user is None or not verify_password(password, user.password_hash):
            raise AuthenticationError("Incorrect username or password")

        access_token = create_access_token(user.user_name)
        # refresh-токен пока не отдаётся клиенту (как и раньше), но генерируется
        create_refresh_token(user.user_name)
        return Token(access_token=access_token, token_type="bearer")

    @staticmethod
    def logout(refresh_token: str) -> None:
        revoked_refresh_tokens.add(refresh_token)

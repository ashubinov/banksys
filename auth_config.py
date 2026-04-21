
from authx import AuthX, AuthXConfig

config = AuthXConfig(
    JWT_SECRET_KEY="SECRET_KEY",
    JWT_ACCESS_COOKIE_NAME="my_access_token",
    JWT_TOKEN_LOCATION= ["headers", "cookies"],
    JWT_COOKIE_CSRF_PROTECT=False,
)

security = AuthX(config=config)
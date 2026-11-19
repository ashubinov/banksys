from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class DatabaseConfig(BaseModel):
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(column_0_label)s",
        "ck": "ck_%(column_0_label)s",
        "fk": "fk_%(table_name)s_%(column_0_label)s",
        "pk": "pk_%(table_name)s",
    }


class ApiPrefix(BaseModel):
    auth: str = "/oauth"
    client: str = "/client"
    deposit: str = "/deposit"
    account: str = "/account"

    @property
    def token_url(self) -> str:
        # путь для OAuth2PasswordBearer (без ведущего слэша, как было раньше)
        return self.auth.lstrip("/") + "/token"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # переменные окружения (имена совпадают с .env / .env.example)
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    database_url: str
    admin_first_username: str
    admin_first_password: str

    # вложенные настройки со значениями по умолчанию
    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig()
    api: ApiPrefix = ApiPrefix()


settings = Settings()

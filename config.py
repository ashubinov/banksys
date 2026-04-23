from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm:str
    access_token_expire_minutes: int = 30  # Авто-конвертация из строки в int
    database_url: str
    refresh_token_expire_days: int = 7
    admin_first_username: str
    admin_first_password: str
    class Config:
        env_file = ".env"

settings = Settings()

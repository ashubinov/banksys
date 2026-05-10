from datetime import datetime

from pydantic import BaseModel
from models import UserRole

class DepositAddShema(BaseModel):
    deposit_name: str
    shelf_life: int
    rate: float

class DepositShema(DepositAddShema):
    deposit_id: int

class DepositPatchShema(BaseModel):
    deposit_name: str | None = None
    shelf_life: int | None = None
    rate: float | None = None


class UserCreateSchema(BaseModel):
    username: str
    password: str
    role: UserRole

class LoginRequestSchema(BaseModel):
    username: str
    password: str

class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str="Bearer"

class UserOutSchema(BaseModel):
    user_id: int
    user_name: str
    role: UserRole


class ClientAddShema(BaseModel):
    client_name: str
    client_patronymic: str
    client_surname: str
    passport_numb: str
    city: str
    phone_numb: str

class ClientSchema(ClientAddShema):
    client_id: int

class ClientPatchShema(BaseModel):
    client_name: str | None = None
    client_patronymic: str | None = None
    client_surname: str | None = None
    passport_numb: str | None = None
    city: str | None = None
    phone_numb: str | None = None

class AccountAddShema(BaseModel):
    opening_date: datetime
    closing_date: datetime | None = None
    amount_invested: int
    deposit_id: int
    client_id: int

class AccountShema(AccountAddShema):
    account_numb: int

class AccountPatchShema(BaseModel):
    opening_date: datetime | None = None
    closing_date: datetime | None = None
    amount_invested: int | None = None
    deposit_id: int | None = None
    client_id: int | None = None

class Token(BaseModel):
    access_token: str
    token_type: str
    token_type: str

class TokenData(BaseModel):
    username: str
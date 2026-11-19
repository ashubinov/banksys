from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AccountAddShema(BaseModel):
    opening_date: datetime
    closing_date: datetime | None = None
    amount_invested: int
    deposit_id: int
    client_id: int


class AccountShema(AccountAddShema):
    model_config = ConfigDict(from_attributes=True)

    account_numb: int


class AccountPatchShema(BaseModel):
    opening_date: datetime | None = None
    closing_date: datetime | None = None
    amount_invested: int | None = None
    deposit_id: int | None = None
    client_id: int | None = None

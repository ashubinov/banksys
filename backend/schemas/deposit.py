from pydantic import BaseModel, ConfigDict


class DepositAddShema(BaseModel):
    deposit_name: str
    shelf_life: int
    rate: float


class DepositShema(DepositAddShema):
    model_config = ConfigDict(from_attributes=True)

    deposit_id: int


class DepositPatchShema(BaseModel):
    deposit_name: str | None = None
    shelf_life: int | None = None
    rate: float | None = None

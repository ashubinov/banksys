from fastapi import APIRouter

from backend.core.config import settings
from backend.dependencies import DepositManagerDep, DepositServiceDep
from backend.schemas import DepositAddShema, DepositPatchShema, DepositShema

router = APIRouter(prefix=settings.api.deposit, tags=["deposit"])


@router.post("/new")
async def add_deposit(
    data: DepositAddShema,
    service: DepositServiceDep,
    user: DepositManagerDep,
):
    await service.create(data)
    return {"ok": True}


@router.patch("/{deposit_id}")
async def update_deposit(
    deposit_id: int,
    data: DepositPatchShema,
    service: DepositServiceDep,
    user: DepositManagerDep,
):
    deposit = await service.update(deposit_id, data)
    return {"ok": True, "deposit": deposit}


@router.delete("/{deposit_id}")
async def remove_deposit(
    deposit_id: int,
    service: DepositServiceDep,
    user: DepositManagerDep,
):
    await service.delete(deposit_id)
    return {"ok": True, "message": "delete successful"}


@router.get("/{deposit_id}", response_model=DepositShema)
async def get_deposit_byid(deposit_id: int, service: DepositServiceDep):
    return await service.get(deposit_id)


@router.get("/", response_model=list[DepositShema])
async def get_deposit_all(service: DepositServiceDep):
    return await service.get_all()

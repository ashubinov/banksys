from orm import AsyncORM
from fastapi import APIRouter, Depends, HTTPException
from schemas import DepositAddShema, DepositPatchShema, DepositShema
from database import SessionDep
from models import UserRole
from role import require_role

router =APIRouter(prefix="/deposit", tags=["deposit"])
@router.post("/new")
async def add_deposit(
        data: DepositAddShema,
        session: SessionDep,
        user = Depends(require_role(
            UserRole.deposit_manager,
            UserRole.admin
        ))
        ):
    await AsyncORM.add_new_deposit(data, session)
    return {"ok": True}

@router.patch("/{deposit_id}")
async def update_deposit(
        deposit_id: int,
        data: DepositPatchShema,
        session: SessionDep,
        user = Depends(require_role(UserRole.deposit_manager, UserRole.admin))
):
    updat_deposit = await AsyncORM.update_deposit(session, deposit_id, data)
    if not updat_deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    return {"ok": True, "deposit": updat_deposit}


@router.delete("/{deposit_id}")
async def remove_deposit(
        deposit_id: int,
        session: SessionDep,
        user = Depends(require_role(UserRole.deposit_manager, UserRole.admin))
):
    res = await AsyncORM.delete_deposit(session, deposit_id)
    if not res:
        raise HTTPException(status_code=404, detail="Deposit not found")
    return {"ok": True, "message": "delete successful"}

@router.get("/{deposit_id}", response_model=DepositShema)
async def get_deposit_byid(deposit_id: int, session: SessionDep):
    deposit = await AsyncORM.get_deposit_by_id(session, deposit_id)
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit not found")
    return deposit

@router.get("/", response_model=list[DepositShema])
async def get_deposit_all(session: SessionDep):
    deposits= await AsyncORM.get_all_deposits(session)
    return deposits
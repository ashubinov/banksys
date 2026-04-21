
from orm import AsyncORM
from fastapi import APIRouter, Depends, HTTPException
from schemas import AccountAddShema, AccountShema, AccountPatchShema
from database import SessionDep
from models import UserRole
from role import require_role

router =APIRouter(prefix="/account", tags=["account"])
@router.post("/new")
async def create_acc(
        data: AccountAddShema,
        session: SessionDep,
        user = Depends(require_role(UserRole.bank_operator, UserRole.admin))
):
    await  AsyncORM.add_account(session, data)
    return {"message": "client created successfully"}

@router.get("/{account_numb}", response_model=AccountShema)
async def get_acc_bynumb(account_numb: int, session: SessionDep):
    account = await AsyncORM.get_account_by_numb(session, account_numb)
    if not account:
        raise HTTPException(status_code=404, detail="Client not found")
    return account

@router.get("/", response_model=list[AccountShema])
async def get_all_acc(session: SessionDep):
    accounts = await AsyncORM.get_account_all(session)
    return accounts

@router.patch("/{account_numb}")
async def update_account(
        session: SessionDep,
        account_numb: int,
        data: AccountPatchShema,
        user = Depends(require_role(UserRole.bank_operator, UserRole.admin))
):
    up_acc = await AsyncORM.update_account(session, account_numb, data)
    if not up_acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"ok": True, "client": up_acc}

@router.delete("/{account_numb}")
async def delete_acc(
        session: SessionDep,
        account_numb: int,
        user = Depends(require_role(UserRole.bank_operator, UserRole.admin))
):
    delete = await AsyncORM.delete_account(session, account_numb)
    if not delete:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "deleted successfully"}
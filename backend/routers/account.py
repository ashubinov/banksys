from fastapi import APIRouter

from backend.core.config import settings
from backend.dependencies import AccountServiceDep, OperatorDep
from backend.schemas import AccountAddShema, AccountPatchShema, AccountShema

router = APIRouter(prefix=settings.api.account, tags=["account"])


@router.post("/new")
async def create_acc(
    data: AccountAddShema,
    service: AccountServiceDep,
    user: OperatorDep,
):
    await service.create(data)
    return {"message": "account created successfully"}


@router.get("/{account_numb}", response_model=AccountShema)
async def get_acc_bynumb(account_numb: int, service: AccountServiceDep):
    return await service.get(account_numb)


@router.get("/", response_model=list[AccountShema])
async def get_all_acc(service: AccountServiceDep):
    return await service.get_all()


@router.patch("/{account_numb}")
async def update_account(
    account_numb: int,
    data: AccountPatchShema,
    service: AccountServiceDep,
    user: OperatorDep,
):
    account = await service.update(account_numb, data)
    return {"ok": True, "client": account}


@router.delete("/{account_numb}")
async def delete_acc(
    account_numb: int,
    service: AccountServiceDep,
    user: OperatorDep,
):
    await service.delete(account_numb)
    return {"message": "deleted successfully"}

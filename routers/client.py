from orm import AsyncORM
from fastapi import APIRouter, Depends, HTTPException
from schemas import ClientAddShema, ClientSchema, ClientPatchShema
from database import SessionDep
from models import UserRole
from role import require_role

router =APIRouter(prefix="/client", tags=["client"])
@router.post("/new")
async def create_client(
        data: ClientAddShema,
        session: SessionDep,
        user = Depends(require_role(UserRole.bank_operator, UserRole.admin))
):
    await  AsyncORM.add_client(session, data)
    return {"message": "client created successfully"}

@router.get("/{client_id}", response_model=ClientSchema)
async def get_client_byid(client_id: int, session: SessionDep):
    client = await AsyncORM.get_client_by_id(session, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.get("/", response_model=list[ClientSchema])
async def get_all_clients(session: SessionDep):
    clients = await AsyncORM.get_all_client(session)
    return clients

@router.patch("/{client_id}")
async def update_client(
        session: SessionDep,
        client_id: int,
        data: ClientPatchShema,
        user = Depends(require_role(UserRole.bank_operator, UserRole.admin))
):
    up_client = await AsyncORM.update_client(session, client_id, data)
    if not up_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"ok": True, "client": up_client}

@router.delete("/{client_id}")
async def delete_client(
        session: SessionDep,
        client_id: int,
        user = Depends(require_role(UserRole.bank_operator, UserRole.admin))
):
    delete = await AsyncORM.delete_client(session, client_id)
    if not delete:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "deleted successfully"}
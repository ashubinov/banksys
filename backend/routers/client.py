from fastapi import APIRouter

from backend.core.config import settings
from backend.dependencies import ClientServiceDep, OperatorDep
from backend.schemas import ClientAddShema, ClientPatchShema, ClientSchema

router = APIRouter(prefix=settings.api.client, tags=["client"])


@router.post("/new")
async def create_client(
    data: ClientAddShema,
    service: ClientServiceDep,
    user: OperatorDep,
):
    await service.create(data)
    return {"message": "client created successfully"}


@router.get("/{client_id}", response_model=ClientSchema)
async def get_client_byid(client_id: int, service: ClientServiceDep):
    return await service.get(client_id)


@router.get("/", response_model=list[ClientSchema])
async def get_all_clients(service: ClientServiceDep):
    return await service.get_all()


@router.patch("/{client_id}")
async def update_client(
    client_id: int,
    data: ClientPatchShema,
    service: ClientServiceDep,
    user: OperatorDep,
):
    client = await service.update(client_id, data)
    return {"ok": True, "client": client}


@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    service: ClientServiceDep,
    user: OperatorDep,
):
    await service.delete(client_id)
    return {"message": "deleted successfully"}

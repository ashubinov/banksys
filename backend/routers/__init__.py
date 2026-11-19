from fastapi import APIRouter

from . import account, auth, client, deposit

router = APIRouter()
router.include_router(auth.router)
router.include_router(client.router)
router.include_router(deposit.router)
router.include_router(account.router)

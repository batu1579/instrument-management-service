from fastapi import APIRouter

from app.api.v1 import router as v1_router

root_router = APIRouter(prefix="/api")
root_router.include_router(v1_router)

from fastapi import APIRouter

from app.api.api_v1.endpoints import map
from app.api.api_v1.endpoints import cap
# from app.api.api_v1.endpoints import misc


api_router = APIRouter()
api_router.include_router(map.router, prefix="/map", tags=["map"])
api_router.include_router(cap.router, prefix="/cap", tags=["cap"])
# api_router.include_router(misc.router, prefix="/misc", tags=["misc"])

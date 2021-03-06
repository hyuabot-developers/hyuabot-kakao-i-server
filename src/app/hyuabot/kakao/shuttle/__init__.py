from fastapi import APIRouter

from app.hyuabot.kakao.shuttle.arrival import shuttle_arrival_router
from app.hyuabot.kakao.shuttle.stop import shuttle_stop_router

shuttle_router = APIRouter(prefix="/shuttle")
shuttle_router.include_router(shuttle_arrival_router)
shuttle_router.include_router(shuttle_stop_router)

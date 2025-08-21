from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    equipment,
    equipment_maintenance,
    maintenance_log,
    batch_tracking,
    batch_dispatch,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(equipment.router, prefix="/equipment", tags=["equipment"])
api_router.include_router(equipment_maintenance.router, prefix="/equipment-maintenance", tags=["equipment-maintenance"])
api_router.include_router(maintenance_log.router, prefix="/maintenance-logs", tags=["maintenance-logs"])
api_router.include_router(batch_tracking.router, prefix="/batches", tags=["batches"])
api_router.include_router(batch_dispatch.router, prefix="/batches-dispatch", tags=["batches-dispatch"]) 
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    equipment,
    equipment_maintenance,
    maintenance_log,
    batch_tracking,
    batch_dispatch,
    fermentation_trials,
    quality_control,
    upscales,
    transformation,
    login,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(equipment.router, prefix="/equipment", tags=["equipment"])
api_router.include_router(equipment_maintenance.router, prefix="/equipment-maintenance", tags=["equipment-maintenance"])
api_router.include_router(maintenance_log.router, prefix="/maintenance-logs", tags=["maintenance-logs"])
api_router.include_router(batch_tracking.router, prefix="/batches", tags=["batches"])
api_router.include_router(batch_dispatch.router, prefix="/batches-dispatch", tags=["batches-dispatch"])
api_router.include_router(fermentation_trials.router, prefix="/fermentation-trials", tags=["fermentation-trials"])
api_router.include_router(quality_control.router, prefix="/quality-control", tags=["quality-control"])
api_router.include_router(upscales.router, prefix="/upscales", tags=["upscales"])
api_router.include_router(transformation.router, prefix="/transformation", tags=["transformation"])
api_router.include_router(login.router, prefix="/login", tags=["login"]) 
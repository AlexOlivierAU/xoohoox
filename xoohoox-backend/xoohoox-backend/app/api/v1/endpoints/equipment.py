from fastapi import APIRouter, HTTPException, Depends
from app.api import deps

router = APIRouter()

@router.get("/")
def list_equipment(current_user: str = Depends(deps.get_current_user)):
    """
    List all equipment.
    """
    # Return dummy data for now
    return [
        {"id": "E001", "name": "Fermentation Tank 1", "type": "tank"},
        {"id": "E002", "name": "Fermentation Tank 2", "type": "tank"},
    ] 
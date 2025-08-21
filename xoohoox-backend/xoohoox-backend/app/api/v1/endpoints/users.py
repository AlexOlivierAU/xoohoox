from fastapi import APIRouter, HTTPException, Depends
from app.api import deps

router = APIRouter()

@router.get("/me")
def read_user_me(current_user: str = Depends(deps.get_current_user)):
    """
    Get current user.
    """
    return {"username": current_user} 
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    # For now, accept any credentials
    return {
        "access_token": "dummy_token",
        "token_type": "bearer"
    }

@router.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    """
    Test access token.
    """
    return {"username": "testuser", "token": token} 
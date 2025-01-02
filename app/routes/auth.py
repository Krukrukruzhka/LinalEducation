from fastapi import APIRouter

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from src.utils.auth_utils import create_access_token, decode_token, verify_password, get_password_hash
from src.datamodels.user import User
from config.application import app_settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(tags=["auth"])


# Registrate user
@router.post("/register-user", tags=["unprotected"])
async def register_user(request: Request, user: User):
    existing_user = await app_settings.database.get_user_by_username(user.username)

    if existing_user:
        raise HTTPException(status_code=400, detail="User is exists")

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    await app_settings.database.registrate_user(user)

    return JSONResponse({"msg": "Registration was successful"})


# Authorize user and get token
@router.post("/token", tags=["unprotected"])
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    existing_user = await app_settings.database.get_user_by_username(form_data.username)
    if not existing_user or not verify_password(form_data.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Unknown username or password")

    token_data = {"sub": form_data.username}
    access_token = create_access_token(data=token_data)
    return JSONResponse({"access_token": access_token, "token_type": "bearer"})


# Sample of protected route
@router.get("/protected", tags=["protected"])
async def protected_route(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return JSONResponse({"msg": f"Welcome, {payload['sub']}!"})

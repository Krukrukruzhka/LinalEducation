from fastapi import APIRouter

from fastapi import Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from src.utils.auth_utils import create_access_token, verify_password, get_password_hash, ACCESS_TOKEN_EXPIRE_DAYS, get_token_from_cookie, get_username_by_jwt
from src.datamodels.user import User, RolesEnum
from src.datamodels.auth import RegistrationRequest, LoginRequest
from config.application import app_settings


router = APIRouter(tags=["auth"])


@router.post("/register-user", tags=["unprotected"])
async def register_user(request: Request, response: Response, registration_data: RegistrationRequest):
    existing_user = await app_settings.database.get_user_by_username(registration_data.username)

    if existing_user:
        raise HTTPException(status_code=400, detail="User is exists")

    if registration_data.password != registration_data.repeated_password:
        raise HTTPException(status_code=400, detail="Passwords are different")

    user = User(**dict(registration_data))

    hashed_password = get_password_hash(registration_data.password)
    user.password = hashed_password

    await app_settings.database.registrate_user(user)

    token_data = {"sub": user.username}
    access_token = create_access_token(data=token_data)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {"msg": "Registration was successful"}


@router.get("/login", tags=["html"])
async def login_page(request: Request):
    templates = app_settings.ui.templates

    web_context = {
        "request": request
    }

    return templates.TemplateResponse("login.html", context=web_context)


@router.get("/register", tags=["html"])
async def registrate_page(request: Request):
    templates = app_settings.ui.templates

    web_context = {
        "request": request,
        "RolesEnum": RolesEnum
    }

    return templates.TemplateResponse("register.html", context=web_context)


@router.post("/login-user", tags=["unprotected"])
async def get_token(response: Response, login_data: LoginRequest):
    existing_user = await app_settings.database.get_user_by_username(login_data.username)
    if not existing_user or not verify_password(login_data.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Unknown username or password")

    token_data = {"sub": login_data.username}
    access_token = create_access_token(data=token_data)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age= ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {"message": "Token was issued successfully"}


# Sample of protected route
@router.get("/protected", tags=["protected"])
async def protected_route(token: str = Depends(get_token_from_cookie)):
    return JSONResponse({"msg": f"Welcome, {get_username_by_jwt(token)}!"})


@router.post("/logout", tags=["unprotected"])
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

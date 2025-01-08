from fastapi import Cookie, HTTPException
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from calendar import timegm


SECRET_KEY = "SECRET"  # TODO: add to .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if timegm(datetime.now().utctimetuple()) > payload.get('exp'):
            raise JWTError
        return payload
    except JWTError:
        return None


def get_username_by_jwt(token: str) -> str:
    payload = decode_token(token)
    if payload is None or payload.get('sub', None) is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload['sub']


async def get_token_from_cookie(access_token: str = Cookie(None)) -> str:
    if access_token is None:
        raise HTTPException(status_code=401, detail="No access token provided")
    return access_token

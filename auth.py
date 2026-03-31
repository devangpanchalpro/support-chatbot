import os
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

# Load configuration from .env
load_dotenv()

# ─── API KEY CONFIG ─────────────────────────────────
# Multiple keys supported (comma-separated in .env)
_raw_keys = os.getenv("AAROGYA_API_KEYS", "")
VALID_API_KEYS = [k.strip() for k in _raw_keys.split(",") if k.strip()]

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Validates the API Key from the X-API-KEY header.
    Give this key to any external app that needs to use your chatbot.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key missing. Pass your key in the 'X-API-KEY' header."
        )
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key."
        )
    return api_key


# ─── JWT LOGIC (COMMENTED OUT — NOT IN USE) ─────────
# If you ever need user login with JWT tokens, uncomment below.
#
# import hashlib
# from datetime import datetime, timedelta, timezone
# from typing import Optional
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# import models, database, schemas
#
# SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
# ALGORITHM = "HS256"
# ACCESS_EXP = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
# REFRESH_EXP = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
#
# pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)
#
# def get_password_hash(password: str):
#     h = hashlib.sha256(password.encode('utf-8')).hexdigest()
#     return pwd_context.hash(h)
#
# def verify_password(plain_password: str, hashed_password: str):
#     h = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
#     return pwd_context.verify(h, hashed_password)
#
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_EXP))
#     to_encode.update({"exp": expire, "type": "access"})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
# def create_refresh_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_EXP)
#     to_encode.update({"exp": expire, "type": "refresh"})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
# async def get_current_user(
#     token: Optional[str] = Depends(oauth2_scheme),
#     db: Session = Depends(database.get_db)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username and payload.get("type") == "access":
#             user = db.query(models.User).filter(models.User.username == username).first()
#             if user:
#                 return user.username
#     except JWTError:
#         pass
#     raise credentials_exception

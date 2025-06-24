from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from db import database
from model.user import User
from sqlalchemy.future import select
from sqlalchemy import update, or_
from passlib.context import CryptContext

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24*60*7

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=150)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def access_token_for_func(user, db):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "email": user.email},
        expires_delta=access_token_expires
    )
   
    stmt = update(User).where(User.username == user.username).values(token=access_token)
    await db.execute(stmt)
    await db.commit()
   
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

async def login_for_access_token(db: AsyncSession = Depends(database), form_data: OAuth2PasswordRequestForm = Depends()):
    query = select(User).where(or_(User.email == form_data.username, User.username == form_data.username))
    result = await db.execute(query)
    user = result.scalars().first()
    if user:
        is_validate_password = pwd_context.verify(form_data.password, user.password)
    else:
        is_validate_password = False

        
    if not is_validate_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your username or password is incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
   
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "email": user.email},
        expires_delta=access_token_expires
    )
   
    stmt = update(User).where(User.username == user.username).values(token=access_token)
    await db.execute(stmt)
    await db.commit()
   
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def token_has_expired(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expiration_time = datetime.utcfromtimestamp(payload.get("exp"))  # UTC
        current_time = datetime.utcnow()
        return current_time > expiration_time
    except jwt.JWTError:
        return True  # Если токен невалидный, считаем его истекшим
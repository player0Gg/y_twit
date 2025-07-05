from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from db import database
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from utils.token import login_for_access_token
from schema.tokens import LoginRequest


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*7

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
login_router = APIRouter(tags=['Login and Refresh token'])


# @login_router.post("/api/login")
# async def access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: AsyncSession = Depends(database)):
    # return await login_for_access_token(db, form_data)


@login_router.post("/api/login")
async def access_token(login_data: LoginRequest, db: AsyncSession = Depends(database)):
    # Создаем объект, совместимый с OAuth2PasswordRequestForm
    class FormData:
        def __init__(self, username: str, password: str):
            self.username = username
            self.password = password

    form_data = FormData(login_data.username, login_data.password)
    return await login_for_access_token(db, form_data)
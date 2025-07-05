from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import database
from schema.user import User_cr, User_upd, UserShort
from func.user import get_user_by_username, create_user, update_user, get_all_users_func
from typing import List

user_router = APIRouter()


@user_router.get("/api/all_users", response_model=List[UserShort])
async def get_all_users(username: str=None, db :AsyncSession=Depends(database)):
    return await get_all_users_func(username, db)
 
@user_router.get("/api/user")
async def get_user(username: str, db: AsyncSession = Depends(database)):
    return await get_user_by_username(username, db)


@user_router.post("/api/register")
async def create_user_endpoint(form: User_cr, db: AsyncSession = Depends(database)):
    return await create_user(form, db)


@user_router.put("/api/update/user")
async def update_user_endpoint(form: User_upd, db: AsyncSession = Depends(database)):
    return await update_user(form, db)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import database
from model.user import User
from schema.user import User_cr, User_upd
from func.user import get_user_by_id, create_user, update_user
from router.login import get_current_user

user_router = APIRouter()


@user_router.get("/api/{current_user.id}")
async def get_user(current_user: User=Depends(get_current_user), db: AsyncSession = Depends(database)):
    return await get_user_by_id(current_user.id, db)

@user_router.post("/api/register")
async def create_user_endpoint(form: User_cr, db: AsyncSession = Depends(database)):
    return await create_user(form, db)

@user_router.put("/api/update/{current_user}")
async def update_user_endpoint(form: User_upd, crurrent_user: User=Depends(get_current_user), db: AsyncSession = Depends(database)):
    return await update_user(form, crurrent_user.id, db)
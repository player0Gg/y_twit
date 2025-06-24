from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from db import database
from model.user import User
from schema.user import User_cr, User_upd
from func.user import get_user_by_username, create_user, update_user
from utils.current_user import get_current_user
from utils.image import save_image
from sqlalchemy import update
from sqlalchemy.future import select

user_router = APIRouter()


@user_router.get("/api/user")
async def get_user(username: str, db: AsyncSession = Depends(database)):
    return await get_user_by_username(username, db)

@user_router.post("/api/register")
async def create_user_endpoint(form: User_cr, db: AsyncSession = Depends(database)):
    return await create_user(form, db)

@user_router.put("/api/update/user")
async def update_user_endpoint(form: User_upd, current_user: User=Depends(get_current_user), db: AsyncSession = Depends(database)):
    return await update_user(form, current_user, db)
    
@user_router.post("/api/user_avatar")
async def add_user_avatar(username: str, avatar: UploadFile = str, db: AsyncSession = Depends(database)):
    user=await db.execute(select(User).where(User.username == username))
    result=user.scalar()
    result.avatar = await save_image(avatar)

    await db.commit()
    return await get_user_by_username(username, db)
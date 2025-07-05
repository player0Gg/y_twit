from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import database
from model.user import User
from schema.user import User_friends
from func.friends_subs import add_user_subs_func, delete_user_subs_func
from sqlalchemy.future import select
from utils.unicom import is_friend


fr_router=APIRouter()


@fr_router.put("/api/add_friends")
async def add_user_friends(subs: User_friends, db: AsyncSession = Depends(database)):
    return await add_user_subs_func(subs, db)

@fr_router.post("/api/remove_friends")
async def delete_user_friends(friends: User_friends, db: AsyncSession = Depends(database)):
    return await delete_user_subs_func(friends, db)

@fr_router.get("/api/is_friend_check")
async def get_is_friend(username: str, fr_username: str, db: AsyncSession = Depends(database)):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    query = select(User).where(User.username == fr_username)
    result = await db.execute(query)
    fr_user = result.scalar_one_or_none()

    return await is_friend(user, fr_user)

import os
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db import database
from model.user import User
from func.user import get_user_by_username
from func.images import save_avatar, save_com_image, save_banner
from sqlalchemy.future import select


image_router=APIRouter()


@image_router.get("/api/image/{directory}/{filename}")
async def get_avatar(directory: str ,filename: str):
    file_path = os.path.join(f"images/{directory}", filename)
    print(file_path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Изображение не найдено")


@image_router.post("/api/save_user_avatar")
async def add_user_avatar(username: str=Form(), avatar: UploadFile=File(), db: AsyncSession = Depends(database)):
    user=await db.execute(select(User).where(User.username == username))
    result=user.scalar()
    if result.avatar:
        # If the user already has an avatar, delete the old one
        old_avatar_path = os.path.join("images/avatars", result.avatar)
        if os.path.exists(old_avatar_path)!="default_avatar.jpg":
            os.remove(old_avatar_path)

    result.avatar = await save_avatar(avatar)

    await db.commit()
    return await get_user_by_username(username, db)


@image_router.post("/api/save_user_banner")
async def add_user_banner(username: str=Form(), banner: UploadFile=File(), db: AsyncSession = Depends(database)):
    user=await db.execute(select(User).where(User.username == username))
    result=user.scalar()
    if result.banner:
        # If the user already has an banner, delete the old one
        old_banner_path = os.path.join("images/banners", result.banner)
        if os.path.exists(old_banner_path)!="default_banner.jpg":
            os.remove(old_banner_path)

    result.banner = await save_banner(banner)

    await db.commit()
    return await get_user_by_username(username, db)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schema.notif import Create_notif
from db import database


notif_router=APIRouter()


@notif_router.get("/api/get_notif")
async def get_user_notif(username: str):
    pass


@notif_router.post("/api/add_notif")
async def get_user_notif(notif: Create_notif, db: AsyncSession=Depends(database)):
    pass


@notif_router.delete("/api/add_notif")
async def get_user_notif(username: str, db: AsyncSession=Depends(database)):
    pass



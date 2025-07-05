from model.notif import Notif
from schema.notif import Create_notif
from sqlalchemy.future import select
from sqlalchemy import update
from model.user import User

async def get_notif(username, db):
    query=select(Notif).where(User.username==username)
    
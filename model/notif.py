from sqlalchemy import Column, String, Integer, DateTime
from db import Base

class Notif(Base):
    __tiblename__="notif"

    title=Column(String(50))
    text=Column(String(100))
    username=Column(Integer)
    create_at=Column(DateTime)
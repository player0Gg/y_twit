from sqlalchemy import Column, Integer, String, Text, JSON
from db import Base
from sqlalchemy.ext.mutable import MutableList

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    avatar = Column(String(255), nullable=True)
    token = Column(Text, nullable=True) 
    role = Column(Integer, default=0)
    banner = Column(String(70), nullable=True)
    display_name = Column(String(50), nullable=True, default=username)
    subs = Column(MutableList.as_mutable(JSON), default=list)
    friends = Column(MutableList.as_mutable(JSON), default=list)
    about_me = Column(String(100), nullable=True)
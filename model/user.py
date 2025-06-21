from sqlalchemy import Column, Integer, String
from db import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    avatar = Column(String(255), nullable=True)
    token = Column(String(255), nullable=True)
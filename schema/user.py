from pydantic import BaseModel
from typing import Dict, Any, List

class User_cr(BaseModel):
    username: str
    email: str
    password: str

class User_upd(BaseModel):
    # email: str | None = None
    display_name: str=None
    username: str=None
    about_me: str=None

class UserShort(BaseModel):
    username: str
    avatar_url: str

    class Config:
        orm_mode = True

class Subs(BaseModel):
    username: str

class User_friends(BaseModel):
    username: str
    subs: Subs
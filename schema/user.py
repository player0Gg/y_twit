from pydantic import BaseModel

class User_cr(BaseModel):
    username: str
    email: str
    password: str

class User_upd(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None


from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    id: int
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    username: Optional[str] = None
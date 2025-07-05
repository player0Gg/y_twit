from pydantic import BaseModel
from datetime import datetime

class Create_notif(BaseModel):
    username: int
    title: str
    text: str


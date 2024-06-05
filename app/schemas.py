from pydantic import BaseModel
from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    lastname: str
    email: str
    password: str
    DoB: Optional[date]
    
    class Config:
        orm_mode = True


class Post(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True
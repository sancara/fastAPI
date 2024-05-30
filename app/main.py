from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from . import models
from . database import engine, get_db
import psycopg2
from psycopg2.extras import RealDictCursor


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class User(BaseModel):
    name: str
    lastname: str
    email: str
    password: str
    DoB: Optional[date]


class Post(BaseModel):
    title: str
    content: str


@app.get("/login")
async def loggin_user():
    user = None
    if user:
        return user
    else:
        return {"message": "You are not logged in"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = (models.Post(title=post.title, content=post.content))
    db.add(new_post)
    db.commit()
    # returning
    db.refresh(new_post)
    return {"message": new_post}


@app.post("/users")
def login(user: User):
    data = {"santiago": {"name": "Santiago", "password": "admin1234"}}

    if user.name in data.keys():
        if user.password == data[user.name]["password"]:
            return "You are logged"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Your credentials are incorrect")
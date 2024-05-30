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

    # if the model has much more attributes, it will cause some pain
    # to parse every single column
    # new_post = (models.Post(title=post.title, content=post.content))

    # better approach
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    # returning
    db.refresh(new_post)
    return {"message": new_post}


@app.get("/posts/{id}")
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).one()
    return {"data": post}


@app.post("/users")
def login(user: User):
    data = {"santiago": {"name": "Santiago", "password": "admin1234"}}

    if user.name in data.keys():
        if user.password == data[user.name]["password"]:
            return "You are logged"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Your credentials are incorrect")
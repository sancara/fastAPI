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
    

@app.get("/sqlalchemy")
def get_post_db(db: Session = Depends(get_db)):
    return {"status": "Success"}


@app.get("/login")
async def loggin_user():
    user = None
    if user:
        return user
    else:
        return {"message": "You are not logged in"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO public.posts (title, content) VALUES(%s,%s) 
                   RETURNING *""",
                   (post.title, post.content))
    new_post = cursor.fetchone()
    conn.commit()
    return {"message": new_post}


@app.post("/users")
def login(user: User):
    data = {"santiago": {"name": "Santiago", "password": "admin1234"}}

    if user.name in data.keys():
        if user.password == data[user.name]["password"]:
            return "You are logged"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Your credentials are incorrect")


try:
    # parametrso de la conexión
    # cursor_factory setea el tipo de cursor, en este caso para que nos 
    # devuelva el nombre de las columnas
    # elegimos RealDictCursor, y hay que importarlo.
    # from pyscopg2.extras import RealDictCursor
    conn = psycopg2.connect(host="localhost",
                            database="fastAPI",
                            user="postgres",
                            password="root",
                            cursor_factory=RealDictCursor)

    cursor = conn.cursor()
    print("Successfully connected to db")
except Exception as err:
    print(f"Connection failed with error: {err}")
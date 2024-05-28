from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from datetime import date
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class User(BaseModel):
    name: str
    lastname: str
    email: str
    password: str
    DoB: Optional[date]


@app.get("/login")
async def loggin_user():
    user = None
    if user:
        return user
    else:
        return {"message": "You are not logged in"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your posts...1...2...3"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def post_creation(payload: dict = Body(...)):
    print(payload)
    
    return {"message": "succesfully created post"}


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
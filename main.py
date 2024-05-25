from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from datetime import date

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


@app.post("/posts'")
def post_creation(payload: dict = Body(...)):
    print(payload)

    return {"message": "succesfully created post"}

@app.post("/users")
def login(user: User):
    data = {"santiago": {"name": "Santiago", "password": "admin1234"}}

    if user.name in data.keys():
        if user.password == data[user.name]["password"]:
            return "You are logged"
    return "Your credentials are incorrect"
    
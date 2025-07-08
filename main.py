from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    tags: list[str] | None = []


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/posts")
async def read_posts():
    return {"data": "posts"}


@app.post("/posts")
async def create_post(post: Post):
    return {"msg": "post created", "data": post}

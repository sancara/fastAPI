from fastapi import FastAPI, HTTPException, status
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


@app.get("/posts", status_code=status.HTTP_201_CREATED)
async def read_posts():
    return {"data": "posts"}


@app.get("/posts/{id}")
async def read_post(id: int):
    if id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found"
        )
    return {"data": f"post {id}"}


@app.post("/posts")
async def create_post(post: Post):
    return {"msg": "post created", "data": post}

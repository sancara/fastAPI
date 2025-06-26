from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/posts")
async def read_posts():
    return {"data": "posts"}

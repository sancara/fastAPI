from fastapi import FastAPI


app = FastAPI()


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
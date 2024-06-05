from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from . database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.get("/posts/{id}")
def get_post_by_id(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post:
        return {"data": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"post with id {id} not found")    


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):

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


@app.delete("/posts/{id}")
def delete_post_by_id(id: int, db: Session = Depends(get_db)):

    post_to_delete = db.query(models.Post).filter(models.Post.id == id)

    if post_to_delete.first() == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} not found")

    post_to_delete.delete(synchronize_session=False)
    db.commit()
    return post_to_delete


@app.post("/users", response_model=schemas.User)
def login(user: schemas.User):
    data = {"santiago": {"name": "Santiago", "password": "admin1234"}}

    if user.name in data.keys():
        if user.password == data[user.name]["password"]:
            return "You are logged"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                        detail="Your credentials are incorrect")
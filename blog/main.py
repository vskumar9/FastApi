from typing import List
from fastapi import Depends, FastAPI, status, Response, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models, hashing
from .database import SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['Blogs'])
async def create_blog(request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = models.Blog(title=request.title, body=request.body, user_id = 1)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blogs'])
async def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    db.delete(blog)
    db.commit()
    return {'detail': 'Blog deleted'}

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
async def update_blog(id: int, request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return {'detail': 'Blog updated'}

@app.get('/blog', response_model=List[schemas.ShowBlog], tags=['Blogs']) #response_model=list[schemas.ShowBlog] both are same here
async def read_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['Blogs'])
async def read_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'error': f'Blog with the id {id} is not available' }
    return blog



@app.post('/user', response_model=schemas.ShowUser, tags=['Users'])
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['Users'])
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
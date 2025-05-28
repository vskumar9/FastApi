from fastapi import Depends, FastAPI, status, Response, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models
from .database import SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
async def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    blog = models.Blog(title=request.title, body=request.body)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    db.delete(blog)
    db.commit()
    return {'detail': 'Blog deleted'}

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return {'detail': 'Blog updated'}

@app.get('/blog')
async def read_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200)
async def read_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'error': f'Blog with the id {id} is not available' }
    return blog
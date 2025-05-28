from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(db: Session, request: schemas.BlogBase):
    blog = models.Blog(title=request.title, body=request.body, user_id = 1)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

def update(db: Session, id: int, request: schemas.BlogBase):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return {'detail': 'Blog updated'}

def delete(db: Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    db.delete(blog)
    db.commit()
    return {'detail': 'Blog deleted'}

def get_by_id(db: Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'error': f'Blog with the id {id} is not available' }
    return blog

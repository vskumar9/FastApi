from typing import List
from fastapi import Depends, status, Response, APIRouter
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..repository import blog

router = APIRouter(
    tags=['Blogs'],
    prefix='/blog'   
)

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_blog(request: schemas.BlogBase, db: Session = Depends(get_db)):
    return blog.create(db, request)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: int, db: Session = Depends(get_db)):
    return blog.delete(db, id)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_blog(id: int, request: schemas.BlogBase, db: Session = Depends(get_db)):
    return blog.update(db, id, request)

@router.get('', response_model=List[schemas.ShowBlog]) #response_model=list[schemas.ShowBlog] both are same here
async def read_blog(db: Session = Depends(get_db)):
    return blog.get_all(db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
async def read_blog(id: int, response: Response, db: Session = Depends(get_db)):
    return blog.get_by_id(db, id)

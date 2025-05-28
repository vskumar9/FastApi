from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, models, hashing
from ..database import get_db
from ..repository import user

router = APIRouter(
    tags=['Users'],
    prefix="/users",
)

@router.post('', response_model=schemas.ShowUser)
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(db, request)

@router.get('/{id}', response_model=schemas.ShowUser)
async def get_user(id: int, db: Session = Depends(get_db)):
    return user.get_user(db, id)
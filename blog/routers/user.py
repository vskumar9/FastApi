from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from .oauth2 import get_current_user

from .. import schemas
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
async def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return user.get_user(db, id)
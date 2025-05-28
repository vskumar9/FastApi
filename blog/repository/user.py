from typing import List
from fastapi import Depends, status, Response, HTTPException, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, models, hashing
from ..database import get_db
from ..repository import blog

def create(db: Session, request: schemas.User):
    user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
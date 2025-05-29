from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..schemas import Login
from ..database import get_db
from ..models import User
from ..hashing import Hash
from ..token import create_access_token


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
async def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access_token = create_access_token(data = {'sub': user.email})
    return {'access_token': access_token}    
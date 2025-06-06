from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..token import verify_token

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


async def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": 'Bearer'}
    )
    return verify_token(token, credentials_exception)
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
#from pydantic import BaseModel

from schemes.TokenDataSchema import TokenDataSchema
from schemes.UserSchema import UserSchema
from sqlalchemy.orm import Session

from tools.database import engine, get_db

from decouple import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/login")

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str, db: Session = Depends(get_db)):
    #print('db: ',db)
    from models.UserModel import UserModel
    user = db.query(UserModel).filter(UserModel.username == username)
    return user.first()

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(username,db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchema(username=username)

    except InvalidTokenError:
        raise credentials_exception
    
    username=token_data.username
    
    user = get_user(username,db)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: Annotated[UserSchema, Depends(get_current_user)],):
    return current_user


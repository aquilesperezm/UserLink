


from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models.UserModel import UserModel
from tools.database import engine, get_db, get_connection
from entities.TokenSchema import TokenSchema
from entities.TokenDataSchema import TokenDataSchema
from entities.UserSchema import UserSchema

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
import tools.auth
from datetime import datetime, timedelta, timezone
from decouple import config

user_router = APIRouter(prefix="/v1/user",tags=["User"])

ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES')

@user_router.post("/login", include_in_schema=False)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> TokenSchema:
    
    user = tools.auth.authenticate_user(form_data.username, form_data.password,db)

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = tools.auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return TokenSchema(access_token=access_token, token_type="bearer")
    
@user_router.get("/current_user")
async def read_users_me(current_user: Annotated[UserSchema, Depends(tools.auth.get_current_active_user)]) -> UserSchema:
    return current_user


@user_router.post("/register")
def create(user: UserSchema, db: Session = Depends(get_db)):
    new_user = UserModel(**user.model_dump())
    new_user.password = tools.auth.get_password_hash(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.get("/list")
async def read(db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    all_users = db.query(UserModel).all()
    return all_users



@user_router.delete("/delete/{id}")
async def delete(id:int,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT,current_user = Depends(tools.auth.get_current_active_user)):
    delete_user = db.query(UserModel).filter(UserModel.id == id)
    if delete_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user no finded")
    else:
        delete_user.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 

@user_router.put('/update/{id}')
async def update(id:int, user: UserSchema, db:Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    update_user = db.query(UserModel).filter(UserModel.id == id)
    update_user.first()
    if update_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user no finded with {id}")
    else:
        update_user.update(user.model_dump(), synchronize_session=False)
        db.commit()
    return update_user.first()


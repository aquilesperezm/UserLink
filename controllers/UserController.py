from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models.UserModel import UserModel
#from tools.database import engine, get_db
from tools.db import get_session as get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemes.TokenSchema import TokenSchema
from schemes.UserSchema import UserSchema


from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
import tools.auth
from datetime import datetime, timedelta, timezone
from decouple import config

user_router = APIRouter(prefix="/v1/user",tags=["User"])

ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES')

@user_router.post("/login")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)) -> TokenSchema:
    
    user = await tools.auth.authenticate_user(form_data.username, form_data.password,db)

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
async def create(user: UserSchema, db: AsyncSession = Depends(get_db)) -> UserSchema:
    new_user = UserModel(**user.model_dump())
    new_user.password = tools.auth.get_password_hash(user.password)
    db.add(new_user)
    await db.commit()
    return user


@user_router.get("/list")
async def read(db: AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    #all_users = db.query(UserModel).execution_options(skip_filter=False).all()
    statement = select(UserModel).where(UserModel.is_deleted == False)
    result = await db.execute(statement)
    return result.scalars().all()


@user_router.get("/everything")
async def everything(db: AsyncSession = Depends(get_db)):
    statement = select(UserModel)
    result = await db.execute(statement)
    return result.scalars().all()
    

@user_router.delete("/delete/{id}")
async def delete(id:int,db: AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    result = await db.execute(select(UserModel).filter(UserModel.id == id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_deleted = True
    await db.commit()
    return user


@user_router.delete("/delete_permanent/{id}")
async def delete(id:int,db: AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    result = await db.execute(select(UserModel).filter(UserModel.id == id))
    user = result.scalar()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"message": "User was permanent deleted successfully  "}
 

@user_router.put('/update/{id}')
async def update(id:int, user_update: UserSchema, db:AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    result = await db.execute(select(UserModel).filter(UserModel.id == id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    return user


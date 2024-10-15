from fastapi import APIRouter
from sqlalchemy.future import select
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models.PostModel import PostModel
from models.UserModel import UserModel
from tools.db import get_session as get_db
from schemes.TokenSchema import TokenSchema
from schemes.PostSchema import PostSchema
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
import tools.auth
from datetime import datetime, timedelta, timezone
from decouple import config

post_router = APIRouter(prefix="/v1/post",tags=["Post"])
 
@post_router.post("/create")
async def create(post: PostSchema, db: AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    
    user_query = select(UserModel).where(UserModel.id == post.user_id)
    user = (await db.execute(user_query)).scalar()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User no finded with {id}")
    else:
        new_post = PostModel(**post.model_dump())
        db.add(new_post)
        await db.commit()
    return new_post


@post_router.get("/list")
async def read(db: AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    statement = select(PostModel).where(PostModel.is_deleted == False)
    result = await db.execute(statement)
    return result.scalars().all()

@post_router.get("/everything")
async def everything(db: AsyncSession = Depends(get_db)):
    statement = select(PostModel)
    result = await db.execute(statement)
    return result.scalars().all()

@post_router.put('/update/{id}')
async def update(id:int, post: PostSchema, db:AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    
    post_query = select(PostModel).where(PostModel.id == id)
    update_post = (await db.execute(post_query)).scalar()
    
    user_query = select(UserModel).where(UserModel.id == post.user_id)
    user = (await db.execute(user_query)).scalar()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user no finded with"+post.user_id)
    
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post no finded with {id}") 
    
    if user and update_post:
        
        for field, value in post.model_dump(exclude_unset=True).items():
            setattr(update_post, field, value)
        
        await db.commit()
    return update_post

@post_router.delete("/delete/{id}")
async def delete(id:int,db: AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    result = await db.execute(select(PostModel).filter(PostModel.id == id))
    post = result.scalars().first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post.is_deleted = True
    await db.commit()
    return post
 
@post_router.delete("/delete_permanent/{id}")
async def delete(id:int,db: AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    result = await db.execute(select(PostModel).filter(PostModel.id == id))
    post = result.scalar()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    await db.delete(post)
    await db.commit()
    return {"message": "Post was permanent deleted successfully  "}



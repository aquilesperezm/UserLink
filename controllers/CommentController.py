
from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models.CommentModel import CommentModel
from models.PostModel import PostModel
from sqlalchemy.future import select

from tools.db import get_session as get_db
from schemes.TokenSchema import TokenSchema
from schemes.CommentSchema import CommentSchema
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
import tools.auth
from datetime import datetime, timedelta, timezone
from decouple import config

# creating a var for import router
comment_router = APIRouter(prefix="/v1/comment",tags=["Comment"])

@comment_router.post("/create")
async def create(comment: CommentSchema, db: AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    new_comment = CommentModel(**comment.model_dump())
    db.add(new_comment)
    await db.commit()
    return new_comment


@comment_router.get("/list")
async def read(db: AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    statement = select(CommentModel).where(CommentModel.is_deleted == False)
    result = await db.execute(statement)
    return result.scalars().all()

@comment_router.get("/everything")
async def everything(db: AsyncSession = Depends(get_db)):
    statement = select(CommentModel)
    result = await db.execute(statement)
    return result.scalars().all()

@comment_router.put('/update/{id}')
async def update(id:int, comment: CommentSchema, db:AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
   
    post_query = select(PostModel).where(PostModel.id == comment.post_id)
    update_post = (await db.execute(post_query)).scalar()
    
    comment_query = select(CommentModel).where(CommentModel.id == id)
    update_comment = (await db.execute(comment_query)).scalar()
    
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no finded with " + str(comment.post_id))
    
    if update_comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment no finded with {id}")
    
    if update_post and update_comment:
        
        for field, value in comment.model_dump(exclude_unset=True).items():
            setattr(update_comment, field, value)
        
        await db.commit()
    return update_comment

@comment_router.delete("/delete/{id}")
async def delete(id:int,db: AsyncSession = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT,current_user = Depends(tools.auth.get_current_active_user)):
    result = await db.execute(select(CommentModel).filter(CommentModel.id == id))
    comment = result.scalars().first()
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    comment.is_deleted = True
    await db.commit()
    return comment
 
 
@comment_router.delete("/delete_permanent/{id}")
async def delete(id:int,db: AsyncSession = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT,current_user = Depends(tools.auth.get_current_active_user)):
    result = await db.execute(select(CommentModel).filter(CommentModel.id == id))
    comment = result.scalar()
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    await db.delete(comment)
    await db.commit()
    return {"message": "Comment was permanent deleted successfully  "}



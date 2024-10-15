


from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models.TagModel import TagModel
from tools.db import get_session as get_db
from schemes.TokenSchema import TokenSchema
from schemes.TagSchema import TagSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
import tools.auth
from datetime import datetime, timedelta, timezone
from decouple import config

tag_router = APIRouter(prefix="/v1/tag",tags=["Tag"])
 
@tag_router.post("/create")
async def create(tag: TagSchema, db: AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    new_tag = TagModel(**tag.model_dump())
    db.add(new_tag)
    await db.commit()
    return new_tag


@tag_router.get("/list")
async def read(db: AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    statement = select(TagModel).where(TagModel.is_deleted == False)
    result = await db.execute(statement)
    return result.scalars().all()

@tag_router.get("/everything")
async def everything(db: AsyncSession = Depends(get_db)):
    statement = select(TagModel)
    result = await db.execute(statement)
    return result.scalars().all()

@tag_router.put('/update/{id}')
async def update(id:int, tag_update: TagSchema, db:AsyncSession = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    result = await db.execute(select(TagModel).filter(TagModel.id == id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for field, value in tag_update.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    return user

@tag_router.delete("/delete/{id}")
async def delete(id:int,db: AsyncSession = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT,current_user = Depends(tools.auth.get_current_active_user)):
    result = await db.execute(select(TagModel).filter(TagModel.id == id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    user.is_deleted = True
    await db.commit()
    return user
 

@tag_router.delete("/delete_permanent/{id}")
async def delete(id:int,db: AsyncSession = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT,current_user = Depends(tools.auth.get_current_active_user)):
    result = await db.execute(select(TagModel).filter(TagModel.id == id))
    user = result.scalar()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"message": "Tag was permanent deleted successfully  "}




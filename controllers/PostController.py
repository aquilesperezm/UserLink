


from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models.PostModel import PostModel
from models.UserModel import UserModel
from tools.database_deprecated import engine, get_db, get_connection
from entities.TokenSchema import TokenSchema
from entities.PostSchema import PostSchema

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
import tools.auth
from datetime import datetime, timedelta, timezone
from decouple import config

post_router = APIRouter(prefix="/v1/post",tags=["Post"])
 
@post_router.post("/create")
def create(post: PostSchema, db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    user = db.query(UserModel).get(post.user_id)
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user no finded with {id}")
    else:
        new_post = PostModel(**post.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    return new_post


@post_router.get("/list")
async def read(db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    all_posts =  db.query(PostModel).execution_options(skip_filter=False).all()
    return all_posts

@post_router.get("/everything")
async def everything(db: Session = Depends(get_db)):
    return db.query(PostModel).execution_options(skip_filter=True).all()

@post_router.put('/update/{id}')
async def update(id:int, post: PostSchema, db:Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    
    update_post = db.query(PostModel).filter(PostModel.id == id)
    user = db.query(UserModel).get(post.user_id) 
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user no finded with"+post.user_id)
    
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post no finded with {id}") 
    
    if user and update_post:
        update_post.update(post.model_dump(), synchronize_session=False)
        db.commit()
    return update_post.first()

@post_router.delete("/delete/{id}")
async def delete(id:int,db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    delete_post = db.query(PostModel).filter(PostModel.id == id)
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post no finded with {id}")
    else:
        delete_post.is_delete = True
        db.add(delete_post)
        db.commit()
        db.refresh(delete_post)
    return Response(status_code=status.HTTP_200_OK)
 
@post_router.delete("/delete_permanent/{id}")
async def delete(id:int,db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    delete_post = db.query(PostModel).filter(PostModel.id == id)
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post no finded with {id}")
    else:
        delete_post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_200_OK)



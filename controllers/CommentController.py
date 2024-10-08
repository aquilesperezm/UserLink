


from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models.CommentModel import CommentModel
from models.PostModel import PostModel

from tools.database_deprecated import engine, get_db, get_connection
from entities.TokenSchema import TokenSchema
from entities.CommentSchema import CommentSchema

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
import tools.auth
from datetime import datetime, timedelta, timezone
from decouple import config

comment_router = APIRouter(prefix="/v1/comment",tags=["Comment"])

@comment_router.post("/create")
def create(comment: CommentSchema, db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    new_comment = CommentModel(**comment.model_dump())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

 
@comment_router.get("/list")
async def read(db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    all_comments = db.query(CommentModel).execution_options(skip_visibility_filter=False).all()
    return all_comments

@comment_router.get("/everything")
async def everything(db: Session = Depends(get_db)):
    return db.query(CommentModel).execution_options(skip_visibility_filter=True).all()

@comment_router.put('/update/{id}')
async def update(id:int, comment: CommentSchema, db:Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    update_comment = db.query(CommentModel).filter(CommentModel.id == id)
    update_comment.first()
    
    post = db.query(PostModel).get(comment.post_id)
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post no finded with " + str(comment.post_id))
    
    if update_comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment no finded with {id}")
    
    if post and update_comment:
        update_comment.update(comment.model_dump(), synchronize_session=False)
        db.commit()
    return update_comment.first()

@comment_router.delete("/delete/{id}")
async def delete(id:int,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT,current_user = Depends(tools.auth.get_current_active_user)):
    delete_comment = db.query(CommentModel).filter(CommentModel.id == id)
    if delete_comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user no finded")
    else:
        delete_comment.is_delete = True
        db.add(delete_comment)
        db.commit()
        db.refresh(delete_comment)
    return Response(status_code=status.HTTP_200_OK)
 
 
@comment_router.delete("/delete_permanent/{id}")
async def delete(id:int,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT,current_user = Depends(tools.auth.get_current_active_user)):
    delete_comment = db.query(CommentModel).filter(CommentModel.id == id)
    if delete_comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user no finded")
    else:
        delete_comment.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_200_OK)






from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models.PostModel import PostModel
from tools.database import engine, get_db, get_connection
from entities.TokenSchema import TokenSchema
from entities.PostSchema import Postschema

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
import tools.auth
from datetime import datetime, timedelta, timezone
from decouple import config

post_router = APIRouter(prefix="/v1/post",tags=["Post"])
 
@post_router.post("/create")
def create(post: Postschema, db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    new_post = PostModel(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@post_router.get("/read")
async def read(db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    all_users = db.query(PostModel).all()
    return all_users

@post_router.put('/update/{id}')
async def update(id:int, user: Postschema, db:Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    update_user = db.query(PostModel).filter(PostModel.id == id)
    update_user.first()
    if update_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user no finded with {id}")
    else:
        update_user.update(user.model_dump(), synchronize_session=False)
        db.commit()
    return update_user.first()

@post_router.delete("/delete/{id}")
async def delete(id:int,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT,current_user = Depends(tools.auth.get_current_active_user)):
    delete_user = db.query(PostModel).filter(PostModel.id == id)
    if delete_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user no finded")
    else:
        delete_user.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 




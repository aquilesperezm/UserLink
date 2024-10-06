


from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models.UserModel import UserModel
from tools.database import engine, get_db, get_connection
from entities.TokenSchema import TokenSchema
from entities.UserSchema import UserSchema

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
import tools.auth
from datetime import datetime, timedelta, timezone
from decouple import config

tag_router = APIRouter(prefix="/v1/tag",tags=["Tag"])
 
@tag_router.post("/create")
def create(user: UserSchema, db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    new_user = UserModel(**user.model_dump())
    new_user.password = tools.auth.get_password_hash(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@tag_router.get("/read")
async def read(db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    all_users = db.query(UserModel).all()
    return all_users

@tag_router.put('/update/{id}')
async def update(id:int, user: UserSchema, db:Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    update_user = db.query(UserModel).filter(UserModel.id == id)
    update_user.first()
    if update_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user no finded with {id}")
    else:
        update_user.update(user.model_dump(), synchronize_session=False)
        db.commit()
    return update_user.first()

@tag_router.delete("/delete/{id}")
async def delete(id:int,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT,current_user = Depends(tools.auth.get_current_active_user)):
    delete_user = db.query(UserModel).filter(UserModel.id == id)
    if delete_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user no finded")
    else:
        delete_user.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 




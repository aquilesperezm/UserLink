


from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models.TagModel import TagModel
from tools.database import engine, get_db
from entities.TokenSchema import TokenSchema
from entities.TagSchema import TagSchema

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
import tools.auth
from datetime import datetime, timedelta, timezone
from decouple import config

tag_router = APIRouter(prefix="/v1/tag",tags=["Tag"])
 
@tag_router.post("/create")
def create(tag: TagSchema, db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    new_tag = TagModel(**tag.model_dump())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


@tag_router.get("/list")
async def read(db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    all_tags = db.query(TagModel).execution_options(skip_filter=False).all()
    return all_tags

@tag_router.get("/everything")
async def everything(db: Session = Depends(get_db)):
    return db.query(TagModel).execution_options(skip_filter=True).all()

@tag_router.put('/update/{id}')
async def update(id:int, tag: TagSchema, db:Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    update_tag = db.query(TagModel).filter(TagModel.id == id)
    if update_tag == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag no finded with {id}")
    else:
        update_tag.update(tag.model_dump(), synchronize_session=False)
        db.commit()
    return update_tag.first()

@tag_router.delete("/delete/{id}")
async def delete(id:int,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT,current_user = Depends(tools.auth.get_current_active_user)):
    delete_tag = db.query(TagModel).filter(TagModel.id == id)
    if delete_tag == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag no finded")
    else:
        delete_tag.is_delete = True
        db.add(delete_tag)
        db.commit()
        db.refresh(delete_tag)
    return Response(status_code=status.HTTP_200_OK)
 

@tag_router.delete("/delete_permanent/{id}")
async def delete(id:int,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT,current_user = Depends(tools.auth.get_current_active_user)):
    delete_tag = db.query(TagModel).filter(TagModel.id == id)
    if delete_tag == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag no finded")
    else:
        delete_tag.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_200_OK)




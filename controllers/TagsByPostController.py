


from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from models.TagModel import TagModel
from tools.database import engine, get_db, get_connection
from entities.TokenSchema import TokenSchema
from entities.TagSchema import TagSchema

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
import tools.auth
from datetime import datetime, timedelta, timezone
from decouple import config

tags_by_post_router = APIRouter(prefix="/v1/tagsbypost",tags=["Tags by Post"])
 
@tags_by_post_router.post("/add_tag_to_post")
def create(tag: TagSchema, db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    new_tag = TagModel(**tag.model_dump())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


@tags_by_post_router.get("/list_by_post/{idpost}")
async def read(db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    all_tags = db.query(TagModel).all()
    return all_tags

'''
@tags_by_post_router.put('/update/{id}')
async def update(id:int, tag: TagSchema, db:Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    update_tag = db.query(TagModel).filter(TagModel.id == id)
    if update_tag == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag no finded with {id}")
    else:
        update_tag.update(tag.model_dump(), synchronize_session=False)
        db.commit()
    return update_tag.first()
'''

@tags_by_post_router.delete("/delete/{id}")
async def delete(id:int,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT,current_user = Depends(tools.auth.get_current_active_user)):
    delete_tag = db.query(TagModel).filter(TagModel.id == id)
    if delete_tag == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag no finded")
    else:
        delete_tag.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_200_OK)
 




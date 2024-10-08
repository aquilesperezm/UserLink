


from fastapi import APIRouter

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from tools.database import engine, get_db
from entities.TokenSchema import TokenSchema
from entities.TagSchema import TagSchema
from entities.TagsByPostSchema import TagsByPostSchema

from models.PostModel import PostModel
from models.TagModel import TagModel
#from models.TagModel import association_table

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
import tools.auth
from datetime import datetime, timedelta, timezone
from decouple import config

tags_by_post_router = APIRouter(prefix="/v1/tagsbypost",tags=["Tags by Post"])
 
@tags_by_post_router.post("/add_tag_to_post")
def create(tbp: TagsByPostSchema, db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    #new_tbp = TagsByPostModel(**tbp.model_dump())
    post = db.query(PostModel).filter(PostModel.id == tbp.idpost).first()
    tag = db.query(TagModel).get(tbp.idtag)
    
    post.tags_posts.append(tag)
    db.add(post)
    db.commit()
    return Response(status_code=status.HTTP_200_OK)    
    


@tags_by_post_router.get("/list_tags_by_post/{idpost}")
async def read(idpost:int,db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    #all_tags = db.query(PostModel).all()
    post = db.query(PostModel).filter(PostModel.id == idpost).first()
    all_tags = post.tags_posts
    
    return all_tags

@tags_by_post_router.get("/list_posts_by_tag/{idtag}")
async def read(idtag:int,db: Session = Depends(get_db),current_user = Depends(tools.auth.get_current_active_user)):
    tag = db.query(TagModel).filter(TagModel.id == idtag).first()
    all_posts = tag.posts_tags
    return all_posts

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

@tags_by_post_router.delete("/delete_by_post/{idpost}")
async def delete(idpost:int,db: Session = Depends(get_db), status_code = status.HTTP_204_NO_CONTENT,current_user = Depends(tools.auth.get_current_active_user)):
    delete_post = db.query(PostModel).filter(PostModel.id == idpost).first()
    delete_post.tags_posts.clear()
   
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag no finded")
    else:
        db.delete(delete_post)
        db.commit()
    return Response(status_code=status.HTTP_200_OK)
 




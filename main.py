from fastapi import FastAPI, Depends, HTTPException, status, Response
import models
from sqlalchemy.orm import Session
#from database import engine, get_db, get_connection
#from schemas import UserSchema, UserSchema,TaskSchema, Token, TokenData
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
import tools.auth
from datetime import datetime, timedelta, timezone
from decouple import config
import uvicorn
from tools.database import get_connection
from models import UserModel,PostModel, CommentModel, TagModel
from controllers import UserController, PostController, CommentController, TagController

from tools.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
  
SERVER_HOSTNAME = config('SERVER_HOSTNAME')
SERVER_PORT = config('SERVER_PORT')

# Test connection
con = get_connection()
  
RESET_FACTORY =  config('RESET_FACTORY')
#print('env: ',RESET_FACTORY)

if RESET_FACTORY == '1':
    print('Log: Recreating Database')
    print('Log: Droping all Tables -  Database')
    Base.metadata.drop_all(bind=engine)
    print('Log: Create all Tables -  Database')
    Base.metadata.create_all(bind=engine)
 
app = FastAPI(
    #openapi_tags=tags_metadata,
    title="UserLink - API Documentation",
    description="API endpoints",
    version="0.1",
    #docExpansion="None"
) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserController.user_router)
app.include_router(PostController.post_router)
app.include_router(CommentController.comment_router)
app.include_router(TagController.tag_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=SERVER_HOSTNAME, port=int(SERVER_PORT), reload=True)

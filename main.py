from fastapi import FastAPI, Depends, HTTPException, status, Response, Request
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
from models import UserModel,PostModel, CommentModel, TagModel
from controllers import UserController, PostController, CommentController, TagController, TagsByPostController
import asyncio
from tools.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

import time
import tools.database
from tools.database import create_tables
from tools.database import connect_db
from tools.database import disconnect_db
from tools.database import metadata,engine
  
SERVER_HOSTNAME = config('SERVER_HOSTNAME')
SERVER_PORT = config('SERVER_PORT')

  
PREPARE_DATABASE_FACTORY =  config('PREPARE_DATABASE_FACTORY')

app = FastAPI(
    #openapi_tags=tags_metadata,
    title="UserLink - API Documentation",
    description="API endpoints",
    version="0.1",
    #docExpansion="None"
) 

app.add_event_handler('startup',connect_db)
app.add_event_handler('shutdown',disconnect_db)

async def initial_setup(dropTables=False):     
    await asyncio.create_task(create_tables(dropTables))


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
app.include_router(TagsByPostController.tags_by_post_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print("Time took to process the request and return response is {} sec".format(time.time() - start_time))
    return response

if __name__ == "__main__":
    asyncio.run(initial_setup(dropTables=True)) 
    uvicorn.run("main:app", host=SERVER_HOSTNAME, port=int(SERVER_PORT), reload=True)
    

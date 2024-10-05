from fastapi import FastAPI, Depends, HTTPException, status, Response
import models
from sqlalchemy.orm import Session
#from database import engine, get_db, get_connection
#from schemas import UserSchema, UserSchema,TaskSchema, Token, TokenData
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from psycopg2 import Error, OperationalError
from passlib.context import CryptContext
#import auth
from datetime import datetime, timedelta, timezone
from decouple import config
import uvicorn
from tools.database import get_connection
from models import UserModel
 
SERVER_HOSTNAME = config('SERVER_HOSTNAME')
SERVER_PORT = config('SERVER_PORT')

# Test connection
con = get_connection()

#Base.metadata.drop_all(bind=engine)
#Base.metadata.create_all(bind=engine)

app = FastAPI(
    #openapi_tags=tags_metadata,
    title="UserLink - API Documentation",
    description="API endpoints",
    version="0.1",
    #docExpansion="None"
)

if __name__ == "__main__":
    uvicorn.run("main:app", host=SERVER_HOSTNAME, port=int(SERVER_PORT), reload=True)

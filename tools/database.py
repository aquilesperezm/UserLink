
from sqlalchemy import create_engine, Column, Boolean, event, Connection
from sqlalchemy.orm import sessionmaker, with_loader_criteria, Session, ORMExecuteState
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI, Depends
from models.SoftDeleteModel import SoftDeleteModel
from sqlmodel import SQLModel, create_engine
import sqlalchemy
from decouple import config
import str2bool

DATABASE_HOSTNAME = config('DATABASE_HOSTNAME')
DATABASE_PORT = config('DATABASE_PORT')
DATABASE_USERNAME = config('DATABASE_USERNAME')
DATABASE_PASSWORD = config('DATABASE_PASSWORD')
DATABASE_DBNAME = config('DATABASE_DBNAME')

#DATABASE_URI = "postgresql://postgres:root@localhost:5432/userlink_db"
DATABASE_URI = 'postgresql://'+DATABASE_USERNAME+':'+DATABASE_PASSWORD+'@'+DATABASE_HOSTNAME+':'+DATABASE_PORT+'/'+DATABASE_DBNAME

engine = create_engine(DATABASE_URI,echo=True)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

Metadata = sqlalchemy.MetaData()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 

def start_connection():
    try:
        print('------------------------------- Connecting database ----------------------------------')
        conn = engine.connect() 
    except Exception:
        print('No existe la BD')
        exit()
    return conn

Connec = start_connection()   

def close_connection():
    try:
        print('----------------------------------- Disconnecting database - Good Bye!!! --------------------------------')
        Connec.close()       
    except Exception:
        exit()    

@event.listens_for(SessionLocal, "do_orm_execute")
def _add_filtering_criteria(execute_state):
    skip_filter = execute_state.execution_options.get("skip_filter", False)
    if execute_state.is_select and not skip_filter:
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                SoftDeleteModel,
                lambda cls: cls.is_deleted.is_(False),
                include_aliases=True,
            )
        )
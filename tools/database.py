
from sqlalchemy import create_engine, Column, Boolean, event
from sqlalchemy.orm import sessionmaker, with_loader_criteria, Session, ORMExecuteState
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI, Depends
from models.SoftDeleteModel import SoftDeleteModel
from sqlmodel import SQLModel, create_engine



DATABASE_URL = "postgresql://postgres:root@localhost:5432/userlink_db"

engine = create_engine(DATABASE_URL,echo=True)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def get_connection():
    try:
        conn = engine.connect()
    except Exception:
        print('No existe la BD')
        exit()
    return conn

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
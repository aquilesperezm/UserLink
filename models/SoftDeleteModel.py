from sqlalchemy import create_engine, Column, Boolean, event
from sqlalchemy.orm import sessionmaker, with_loader_criteria, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI, Depends
import datetime
class SoftDeleteModel:
    is_deleted = Column(Boolean, server_default="0")

import str2bool
from decouple import config
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker, with_loader_criteria, Session, ORMExecuteState
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Boolean, event, Connection
from models.SoftDeleteModel import SoftDeleteModel
from sqlalchemy_utils import create_database, database_exists, drop_database

DATABASE_HOSTNAME = config('DATABASE_HOSTNAME')
DATABASE_PORT = config('DATABASE_PORT')
DATABASE_USERNAME = config('DATABASE_USERNAME')
DATABASE_PASSWORD = config('DATABASE_PASSWORD')
DATABASE_DBNAME = config('DATABASE_DBNAME')

#ASYNC_ENVIRONMENT = str2bool.str2bool(config('ASYNC_ENVIRONMENT'))

DB_ASYNC_URI:str = 'postgresql+asyncpg://'+DATABASE_USERNAME+':'+DATABASE_PASSWORD+'@'+DATABASE_HOSTNAME+':'+DATABASE_PORT+'/'+DATABASE_DBNAME

Engine = create_async_engine(
    DB_ASYNC_URI,
    echo=True,
    future=True,
)

Base = declarative_base()
Conne = None

async def create_all_tables():
        async with Engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

async def drop_all_tables():
        async with Engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


async def drop_db():
        async with Engine.begin() as conn:
            await conn.run_sync(drop_database(Engine.url))
            
async def create_db():
        async with Engine.begin() as conn:
            if not database_exists(Engine.url):
                await conn.run_sync(create_database(Engine.url))

async def start_connection():
    try:
        Conn = await Engine.connect() 
    except Exception:
        print('No existe la BD')
        exit()
    return Conn

print('------------------------------- Connecting database ----------------------------------')
Connec = start_connection() 

async def get_session():
    try:
        
        async_session = sessionmaker(Engine, class_=AsyncSession)
        
        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()


def close_connection():
    try:
        print('----------------------------------- Disconnecting database - Good Bye!!! --------------------------------')
        Connec.close()       
    except Exception:
        exit()    

'''       
@event.listens_for(get_session(), "do_orm_execute")
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
'''
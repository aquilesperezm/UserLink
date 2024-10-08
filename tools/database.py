from databases import Database
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy.orm import sessionmaker,with_loader_criteria
from models.SoftDeleteModel import SoftDeleteModel
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from decouple import config
DATABASE_HOSTNAME = config('DATABASE_HOSTNAME')
DATABASE_PORT = config('DATABASE_PORT')
DATABASE_USERNAME = config('DATABASE_USER')
DATABASE_PASSWORD = config('DATABASE_PASSWORD')
DATABASE_DBNAME = config('DATABASE_DBNAME')


#DATABASE_URI = "postgresql+asyncpg://postgres:root@localhost:5432/userlink_db"
DATABASE_URI = 'postgresql+asyncpg://'+DATABASE_USERNAME+':'+DATABASE_PASSWORD+'@'+DATABASE_HOSTNAME+':'+DATABASE_PORT+'/'+DATABASE_DBNAME

database = Database(DATABASE_URI)

metadata = sqlalchemy.MetaData()
engine: AsyncEngine = create_async_engine(DATABASE_URI,echo=True)

async_session: AsyncSession = async_sessionmaker(engine,expire_on_commit=False)

#SessionLocal = sessionmaker(
#    autocommit=False,
#    autoflush=False,
#    bind=engine
#)

Base = declarative_base()

async def connect_db():
    print('------------------------------- Connecting database ----------------------------------')
    await database.connect()
    
async def create_tables(drop=False):
    async with engine.begin() as connection:
        if drop:
            print(' ---------------------------- Dropping all tables --------------------------------')
            await connection.run_sync(Base.metadata.drop_all)
            print(' ---------------------------- Creating all tables --------------------------------')
        await connection.run_sync(Base.metadata.create_all)    

async def disconnect_db():
    print('----------------------------------- Disconnecting database - Good Bye!!! --------------------------------')
    await database.disconnect()


def get_db():
    db = async_session
    try:
        yield db
    finally:
        db.close()
        
#@event.listens_for(async_session, "do_orm_execute")
#def _add_filtering_criteria(execute_state):
#    skip_filter = execute_state.execution_options.get("skip_filter", False)
#    if execute_state.is_select and not skip_filter:
#        execute_state.statement = execute_state.statement.options(
#            with_loader_criteria(
#                SoftDeleteModel,
#                lambda cls: cls.is_deleted.is_(False),
#                include_aliases=True,
#            )
#        )
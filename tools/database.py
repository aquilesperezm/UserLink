from databases import Database
from sqlalchemy import event
import sqlalchemy
from sqlalchemy.orm import sessionmaker,with_loader_criteria
from models.SoftDeleteModel import SoftDeleteModel

DATABASE_URI = "postgresql+asyncpg://postgres:root@localhost:5432/userlink_db"

database = Database(DATABASE_URI)

metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URI)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

async def connect_db():
    print('connecting database')
    await database.connect()

async def disconnect_db():
    print('disconnecting database - Good Bye!!!')
    await database.disconnect()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
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
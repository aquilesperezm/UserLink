from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import func
from sqlalchemy.sql.sqltypes import DateTime
import datetime

class TimeStampsModel:
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] =  mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
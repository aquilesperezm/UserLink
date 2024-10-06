from sqlalchemy import String, Boolean, Integer, Column, text, TIMESTAMP, ForeignKey, DateTime, func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from tools.database import Base, engine
import datetime

class UserModel(Base):  
    __tablename__ = "userlink_user"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] =  mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    #tasks: Mapped[list['Task']] = relationship(back_populates="owner")
    




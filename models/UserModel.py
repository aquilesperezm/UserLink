from sqlalchemy import String, Boolean, Integer, Column, text, TIMESTAMP, ForeignKey, DateTime, func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from tools.database import Base, engine
import datetime
from models.SoftDeleteModel import SoftDeleteModel
from models.TimeStampsModel import TimeStampsModel

class UserModel(Base, SoftDeleteModel,TimeStampsModel):  
    __tablename__ = "userlink_user"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_deleted: Mapped[bool] = mapped_column(nullable=False)
    posts: Mapped[list['PostModel']] = relationship(back_populates="user") # type: ignore
    




from sqlalchemy import String, Boolean, Integer, Column, text, TIMESTAMP, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from tools.database import Base, engine

class User(Base):
    
    __tablename__ = "userlink_user"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    #tasks: Mapped[list['Task']] = relationship(back_populates="owner")
    




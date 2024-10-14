from sqlalchemy.orm import Mapped, mapped_column, relationship
from tools.db import Base
from models.SoftDeleteModel import SoftDeleteModel
from models.TimeStampsModel import TimeStampsModel

class UserModel(Base, SoftDeleteModel,TimeStampsModel):  
    __tablename__ = "userlink_user"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    fullname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    
    posts: Mapped[list['PostModel']] = relationship(back_populates="user") # type: ignore
    




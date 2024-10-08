from sqlalchemy import String, Boolean, Integer, Column, text, TIMESTAMP, ForeignKey, DateTime, func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from tools.database import Base, engine
import datetime

from models.SoftDeleteModel import SoftDeleteModel
from models.TimeStampsModel import TimeStampsModel

class PostModel(Base,SoftDeleteModel, TimeStampsModel):  
    __tablename__ = "userlink_post"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    
   
    user_id: Mapped[int] = mapped_column(ForeignKey("userlink_user.id",onupdate='CASCADE',ondelete='CASCADE'))
    user: Mapped['UserModel'] = relationship(back_populates="posts") # type: ignore
    
    comments: Mapped[list['CommentModel']] = relationship(back_populates="post") # type: ignore
    
    
    from models.TagModel import association_table
    tags_posts: Mapped[list['TagModel']] = relationship( # type: ignore
        secondary=association_table, back_populates="posts_tags"
    )
    
    



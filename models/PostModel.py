from sqlalchemy import String, Boolean, Integer, Column, text, TIMESTAMP, ForeignKey, DateTime, func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from tools.database import Base, engine
import datetime
from models.TagModel import association_table

class PostModel(Base):  
    __tablename__ = "userlink_post"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] =  mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("userlink_user.id",onupdate='CASCADE',ondelete='CASCADE'))
    user: Mapped['UserModel'] = relationship(back_populates="posts") # type: ignore
    
    comments: Mapped[list['CommentModel']] = relationship(back_populates="post") # type: ignore
    
    tags_posts: Mapped[list['TagModel']] = relationship( # type: ignore
        secondary=association_table, back_populates="posts_tags"
    )




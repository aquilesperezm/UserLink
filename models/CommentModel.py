from sqlalchemy import String, Boolean, Integer, Column, text, TIMESTAMP, ForeignKey, DateTime, func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from tools.database import Base, engine
from models.SoftDeleteModel import SoftDeleteModel
from models.TimeStampsModel import TimeStampsModel

class CommentModel(Base,SoftDeleteModel, TimeStampsModel):  
    __tablename__ = "userlink_comment"
    #skip_visibility_filter: False
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    content: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    likes: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[int] = mapped_column(nullable=False)
    
    '''
    post_id: Mapped[int] = mapped_column(ForeignKey("userlink_post.id",onupdate='CASCADE',ondelete='CASCADE'))
    post: Mapped['PostModel'] = relationship(back_populates="comments") # type: ignore
    '''
    




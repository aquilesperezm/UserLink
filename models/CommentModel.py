from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tools.db import Base 
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
    
    # One to Many
    post_id: Mapped[int] = mapped_column(ForeignKey("userlink_post.id",onupdate='CASCADE',ondelete='CASCADE'))
    post: Mapped['PostModel'] = relationship(back_populates="comments") # type: ignore
    
    




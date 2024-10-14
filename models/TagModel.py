from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tools.db import Base
from models.SoftDeleteModel import SoftDeleteModel
from models.TimeStampsModel import TimeStampsModel


# Many to Many Generated Table 
association_table = Table(
    "userlink_rel_tags_by_post",
    Base.metadata,
    Column("idpost", ForeignKey("userlink_post.id",onupdate='CASCADE',ondelete='CASCADE'), primary_key=True),
    Column("idtag", ForeignKey("userlink_tag.id",onupdate='CASCADE',ondelete='CASCADE'), primary_key=True),
)




class TagModel(Base,SoftDeleteModel,TimeStampsModel):  
    __tablename__ = "userlink_tag"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    color: Mapped[str] = mapped_column(nullable=False)
   
    # Many to Many
    posts_tags: Mapped[list['PostModel']] = relationship( # type: ignore
        secondary=association_table, back_populates="tags_posts"
    )
    
   



from pydantic import BaseModel

class CommentSchema(BaseModel):
    content: str
    author: str
    likes: int
    status: int 
    
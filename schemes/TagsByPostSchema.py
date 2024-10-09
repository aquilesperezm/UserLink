from pydantic import BaseModel

class TagsByPostSchema(BaseModel):
    idpost: int
    idtag:  int
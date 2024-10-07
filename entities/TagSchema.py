from pydantic import BaseModel

class TagSchema(BaseModel):
    name: str
    slug: str
    description: str
    color: str
     
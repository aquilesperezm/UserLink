from pydantic import BaseModel

class Postschema(BaseModel):
    title: str
    content: str
    author: str
     
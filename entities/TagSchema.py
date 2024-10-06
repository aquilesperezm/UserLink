from pydantic import BaseModel

class Tagschema(BaseModel):
    name: str
    slug: str
    description: str
    color: str
     
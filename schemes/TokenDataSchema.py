from pydantic import BaseModel

class TokenDataSchema(BaseModel):
    username: str | None = None
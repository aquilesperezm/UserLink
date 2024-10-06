from pydantic import BaseModel

class UserSchema(BaseModel):
    fullname: str
    lastname: str
    username: str
    password: str
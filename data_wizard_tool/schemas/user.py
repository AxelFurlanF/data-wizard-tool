from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    email: str
    username: str
    password: str

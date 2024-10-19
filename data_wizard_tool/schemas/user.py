from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    email: str
    password: str

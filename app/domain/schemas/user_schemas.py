from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str


class CreateUser(UserSchema):
    password: str

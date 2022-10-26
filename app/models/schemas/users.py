from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str


class UserCreate(BaseUser):
    email: str
    password: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

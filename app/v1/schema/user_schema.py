from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


class UserLogin(BaseModel):
    username: str = Field(...,
                          min_length=5,
                          max_length=50,
                          example="myusername")
    password: str = Field(...,
                          min_length=8,
                          max_length=64,
                          example="strongpass")


class UserBase(BaseModel):
    email: EmailStr = Field(..., example="email@mattilda.io")
    username: str = Field(...,
                          min_length=5,
                          max_length=50,
                          example="myusername")


class User(UserBase):
    id: int = Field(..., example="5")


class UserRegister(UserBase):
    password: str = Field(...,
                          min_length=8,
                          max_length=64,
                          example="strongpass")


class UserProfile(BaseModel):
    user_id: int = Field(..., example=1)
    balance: float = Field(..., example=0.0)


class GetProfile(BaseModel):
    user_id: int = Field(..., example=1)

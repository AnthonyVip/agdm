from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from pydantic import condecimal
from datetime import datetime
from app.v1.model.get_engine import CreateEngine


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    email: str
    first_name: Optional[int]
    last_name: Optional[int]
    is_active: int = Field(default=1)
    date_joined: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime]
    profiles: List["Profile"] = Relationship(back_populates="users")


class Profile(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    balance: condecimal(max_digits=11, decimal_places=3) = Field(default=0.000)


def create_db_and_tables():
    EngineClass = CreateEngine()
    SQLModel.metadata.create_all(EngineClass.__open__())

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, BigInteger, ForeignKey
from datetime import datetime


class UserRole:
    Admin = "Админ"
    User = "Пользователь"
    Banned = "Заблокирован"


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: int = Field(sa_column=Column(BigInteger(), primary_key=True))
    username: str | None
    name: str | None
    role: str = Field(default=UserRole.User)
    last_activity: datetime = Field(default=datetime.now())
    registered_at: datetime = Field(default=datetime.now())
    
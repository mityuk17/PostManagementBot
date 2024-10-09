from sqlmodel import SQLModel, Field, UniqueConstraint
from sqlalchemy import Column, BigInteger, ForeignKey
from datetime import datetime


class Channel(SQLModel, table=True):
    __tablename__ = "channels"
    __table_args__ = (
        UniqueConstraint("channel_id", "added_by", name="unique_channel"),
    )
    
    id: int = Field(default=None, primary_key=True)
    channel_id: int = Field(sa_column=Column(BigInteger()))
    added_by: int = Field(sa_column=Column(BigInteger(), ForeignKey("users.id")))
    title: str
    active: bool = Field(default=True)
    added_at: datetime = Field(default=datetime.now())
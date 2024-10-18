from sqlmodel import SQLModel, Field
from sqlalchemy import Column, BigInteger, ForeignKey, ARRAY
from datetime import datetime


class Post(SQLModel, table=True):
    __tablename__ = "posts"
    
    id: int = Field(default=None, primary_key=True)
    messages: list[int] = Field(sa_column=Column(ARRAY(BigInteger())))
    created_by: int = Field(sa_column=Column(BigInteger(), ForeignKey("users.id")))
    target_channel_id: int = Field(sa_column=Column(BigInteger(), ForeignKey("channels.id")))
    button_label: str | None = Field(default=None)
    button_url: str | None = Field(default=None)
    button_subscribed_text: str | None = Field(default=None)
    button_unsubscribed_text: str | None = Field(default=None)
    send_without_notification: bool = Field(default=False)
    post_datetime: datetime = Field(default=datetime.now())
    posted: bool = Field(default=False)
    delete_datetime: datetime | None = Field(default=None)
    deleted: bool = Field(default=False)
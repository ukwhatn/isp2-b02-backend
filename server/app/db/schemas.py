from datetime import datetime

from pydantic import BaseModel


class MessageBase(BaseModel):
    message: str


class MessageResponse(MessageBase):
    pass


class ErrorResponse(MessageBase):
    pass


class ActorBase(BaseModel):
    name: str


class ActorCreate(ActorBase):
    password: str


class ActorPublic(ActorBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ActorLogin(BaseModel):
    name: str
    password: str


class Actor(ActorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    actor_id: int
    pass


class NotePublic(NoteBase):
    id: int
    actor_id: int
    created_at: datetime
    updated_at: datetime

from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped

from .connection import Base


class Actor(Base):
    __tablename__ = "actor"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=False)
    hashed_password = Column(String)

    notes: Mapped["Note"] = relationship("Note", back_populates="actor")
    followers: Mapped["Follower"] = relationship("Follower", back_populates="actor")

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=False)
    content = Column(String, unique=False)
    actor_id = Column(Integer, ForeignKey("actor.id"))
    actor = relationship("Actor", back_populates="notes")

    likes: Mapped["Like"] = relationship("Like", back_populates="note")

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class OutsideActor(Base):
    __tablename__ = "outside_actor"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=False)

    inbox_uri = Column(String, unique=False)
    outbox_uri = Column(String, unique=False)

    likes: Mapped["Like"] = relationship("Like", back_populates="outside_actor")

    followers: Mapped["Follower"] = relationship("Follower", back_populates="outside_actor")

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class Like(Base):
    __tablename__ = "like"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    note_id = Column(Integer, ForeignKey("note.id"))
    note = relationship("Note", back_populates="likes")

    outside_actor_id = Column(Integer, ForeignKey("outside_actor.id"))
    outside_actor = relationship("OutsideActor", back_populates="likes")

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class Follower(Base):
    __tablename__ = "follower"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    actor_id = Column(Integer, ForeignKey("actor.id"))
    actor = relationship("Actor", back_populates="followers")

    outside_actor_id = Column(Integer, ForeignKey("outside_actor.id"))
    outside_actor = relationship("OutsideActor", back_populates="followers")

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

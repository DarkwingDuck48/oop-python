from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pydantic_sqlalchemy.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Связь один-ко-многим с сообщениями
    messages: Mapped[List['Message']] = relationship(
        'Message', back_populates='user', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'User(id={self.id}, username={self.username})'


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    message_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Связь многие-к-одному с пользователем
    user: Mapped['User'] = relationship('User', back_populates='messages')

    def __repr__(self):
        return f'Message(id={self.id}, user_id={self.user_id}, text={self.message_text[:20]}...)'

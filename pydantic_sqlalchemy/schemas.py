from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Для работы с ORM объектами


class MessageBase(BaseModel):
    message_text: str


class MessageCreate(MessageBase):
    user_id: int


class MessageResponse(MessageBase):
    id: int
    user_id: int
    created_at: datetime
    user: UserResponse  # Включаем информацию о пользователе

    model_config = ConfigDict(from_attributes=True)

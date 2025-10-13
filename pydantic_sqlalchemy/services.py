from typing import List, Optional

from sqlalchemy import select

from pydantic_sqlalchemy.database import DatabaseService
from pydantic_sqlalchemy.models import Message, User
from pydantic_sqlalchemy.schemas import (
    MessageCreate,
    MessageResponse,
    UserCreate,
    UserResponse,
)


class UserService:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    def create_user(self, user_data: UserCreate) -> UserResponse:
        """Создает нового пользователя"""
        with self.db_service.get_session() as session:
            # Проверяем уникальность username и email
            existing_user = session.execute(
                select(User).where(
                    (User.username == user_data.username)
                    | (User.email == user_data.email)
                )
            ).scalar_one_or_none()

            if existing_user:
                raise ValueError(
                    "Пользователь с таким username или email уже существует"
                )

            # Создаем пользователя
            user = User(**user_data.model_dump())
            session.add(user)
            session.commit()
            session.refresh(user)

            print(f"✅ Создан пользователь: {user.username}")
            return UserResponse.model_validate(user)

    def get_all_users(self) -> List[UserResponse]:
        """Возвращает всех пользователей"""
        with self.db_service.get_session() as session:
            users = session.execute(select(User)).scalars().all()
            return [UserResponse.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Находит пользователя по ID"""
        with self.db_service.get_session() as session:
            user = session.get(User, user_id)
            return UserResponse.model_validate(user) if user else None


class MessageService:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    def create_message(self, message_data: MessageCreate) -> MessageResponse:
        """Создает новое сообщение"""
        with self.db_service.get_session() as session:
            # Проверяем что пользователь существует
            user = session.get(User, message_data.user_id)
            if not user:
                raise ValueError(f"Пользователь с ID {message_data.user_id} не найден")

            # Создаем сообщение
            message = Message(**message_data.model_dump())
            session.add(message)
            session.commit()
            session.refresh(message)

            print(f"✅ Создано сообщение от {user.username}")
            return MessageResponse.model_validate(message)

    def get_all_messages(self) -> List[MessageResponse]:
        """Возвращает все сообщения с информацией о пользователях"""
        with self.db_service.get_session() as session:
            messages = (
                session.execute(select(Message).join(User).order_by(Message.created_at))
                .scalars()
                .all()
            )

            return [MessageResponse.model_validate(msg) for msg in messages]

    def get_user_messages(self, user_id: int) -> List[MessageResponse]:
        """Возвращает сообщения конкретного пользователя"""
        with self.db_service.get_session() as session:
            messages = (
                session.execute(
                    select(Message)
                    .join(User)
                    .where(Message.user_id == user_id)
                    .order_by(Message.created_at)
                )
                .scalars()
                .all()
            )

            return [MessageResponse.model_validate(msg) for msg in messages]

    def get_conversation_stats(self):
        """Статистика по сообщениям пользователей"""
        with self.db_service.get_session() as session:
            from sqlalchemy import func

            stats = session.execute(
                select(
                    User.username,
                    func.count(Message.id).label("message_count"),
                    func.max(Message.created_at).label("last_message"),
                )
                .join(Message, isouter=True)
                .group_by(User.id)
                .order_by(func.count(Message.id).desc())
            ).all()

            return stats

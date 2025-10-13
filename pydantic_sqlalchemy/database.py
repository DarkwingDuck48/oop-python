from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class DatabaseService:
    def __init__(self, database_url: str = "sqlite:///messenger2.db"):
        self.engine = create_engine(database_url)
        self.session_factory = Session.bind = self.engine

    def create_tables(self):
        """Создает все таблицы в базе данных"""
        Base.metadata.create_all(self.engine)
        print("✅ Таблицы созданы успешно!")

    def get_session(self):
        """Возвращает сессию для работы с БД"""
        return Session(self.engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str):
        self.engine = create_engine(
            url=url,
            pool_pre_ping=True,
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = scoped_session(
            session_factory=self.session_factory,
        )
        return session

    def session_dependency(self):
        session = self.session_factory()
        try:
            yield session
        finally:
            session.close()


db_helper = DatabaseHelper(url=settings.db_url)

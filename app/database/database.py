from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import Config

class DBInit(Config):
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    @classmethod
    def create(cls):
        from app.database.models import Base
        Base.metadata.create_all(bind=cls.engine)

Base = DBInit.Base
SessionLocal = DBInit.SessionLocal
engine = DBInit.engine



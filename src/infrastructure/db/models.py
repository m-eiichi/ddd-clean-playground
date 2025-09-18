"""
ORMモデル（SQLAlchemy）
"""
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class UserModel(Base):
    """ユーザーORMモデル"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(254), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<UserModel(id={self.id}, email='{self.email}', name='{self.name}')>"


# データベース設定
def create_database_engine(database_url: str):
    """データベースエンジンを作成"""
    return create_engine(database_url)


def create_session_factory(engine):
    """セッションファクトリーを作成"""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables(engine):
    """テーブルを作成"""
    Base.metadata.create_all(bind=engine)

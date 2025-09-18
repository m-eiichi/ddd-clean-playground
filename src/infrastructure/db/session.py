"""
データベースセッション管理
"""
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings


class DatabaseSession:
    """データベースセッション管理クラス"""
    
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self) -> Session:
        """データベースセッションを取得"""
        return self.SessionLocal()
    
    def create_tables(self):
        """テーブルを作成"""
        from infrastructure.db.models import Base
        Base.metadata.create_all(bind=self.engine)


# グローバルインスタンス
db_session = DatabaseSession()


def get_db():
    """依存性注入用のデータベースセッション取得関数"""
    db = db_session.get_session()
    try:
        yield db
    finally:
        db.close()

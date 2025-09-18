"""
ユーザーリポジトリの結合テスト
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from domain.models.user import User
from domain.value_objects.email import Email
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.db.models import Base


class TestUserRepositoryIntegration:
    """ユーザーリポジトリの結合テスト"""
    
    @pytest.fixture
    def db_session(self):
        """テスト用データベースセッション"""
        # インメモリSQLiteデータベースを使用
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        yield session
        session.close()
    
    @pytest.fixture
    def user_repository(self, db_session):
        """ユーザーリポジトリ"""
        return UserRepositoryImpl(db_session)
    
    def test_save_new_user(self, user_repository):
        """新規ユーザー保存テスト"""
        email = Email("test@example.com")
        now = datetime.now()
        
        user = User(
            id=None,
            email=email,
            name="テストユーザー",
            created_at=now,
            updated_at=now
        )
        
        saved_user = user_repository.save(user)
        
        assert saved_user.id is not None
        assert saved_user.email == email
        assert saved_user.name == "テストユーザー"
    
    def test_save_existing_user(self, user_repository):
        """既存ユーザー更新テスト"""
        email = Email("test@example.com")
        now = datetime.now()
        
        # 新規ユーザーを作成
        user = User(
            id=None,
            email=email,
            name="テストユーザー",
            created_at=now,
            updated_at=now
        )
        saved_user = user_repository.save(user)
        user_id = saved_user.id
        
        # ユーザーを更新
        saved_user.change_name("更新された名前")
        updated_user = user_repository.save(saved_user)
        
        assert updated_user.id == user_id
        assert updated_user.name == "更新された名前"
        assert updated_user.updated_at > now
    
    def test_find_by_id(self, user_repository):
        """ID検索テスト"""
        email = Email("test@example.com")
        now = datetime.now()
        
        user = User(
            id=None,
            email=email,
            name="テストユーザー",
            created_at=now,
            updated_at=now
        )
        saved_user = user_repository.save(user)
        
        found_user = user_repository.find_by_id(saved_user.id)
        
        assert found_user is not None
        assert found_user.id == saved_user.id
        assert found_user.email == email
        assert found_user.name == "テストユーザー"
    
    def test_find_by_id_not_found(self, user_repository):
        """ID検索（見つからない場合）テスト"""
        found_user = user_repository.find_by_id(999)
        assert found_user is None
    
    def test_find_by_email(self, user_repository):
        """メールアドレス検索テスト"""
        email = Email("test@example.com")
        now = datetime.now()
        
        user = User(
            id=None,
            email=email,
            name="テストユーザー",
            created_at=now,
            updated_at=now
        )
        user_repository.save(user)
        
        found_user = user_repository.find_by_email(email)
        
        assert found_user is not None
        assert found_user.email == email
        assert found_user.name == "テストユーザー"
    
    def test_find_by_email_not_found(self, user_repository):
        """メールアドレス検索（見つからない場合）テスト"""
        email = Email("notfound@example.com")
        found_user = user_repository.find_by_email(email)
        assert found_user is None
    
    def test_find_all(self, user_repository):
        """全件取得テスト"""
        now = datetime.now()
        
        # 複数のユーザーを作成
        user1 = User(
            id=None,
            email=Email("user1@example.com"),
            name="ユーザー1",
            created_at=now,
            updated_at=now
        )
        user2 = User(
            id=None,
            email=Email("user2@example.com"),
            name="ユーザー2",
            created_at=now,
            updated_at=now
        )
        
        user_repository.save(user1)
        user_repository.save(user2)
        
        all_users = user_repository.find_all()
        
        assert len(all_users) == 2
        emails = [user.email.value for user in all_users]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails
    
    def test_delete_user(self, user_repository):
        """ユーザー削除テスト"""
        email = Email("test@example.com")
        now = datetime.now()
        
        user = User(
            id=None,
            email=email,
            name="テストユーザー",
            created_at=now,
            updated_at=now
        )
        saved_user = user_repository.save(user)
        
        # 削除前は存在する
        assert user_repository.find_by_id(saved_user.id) is not None
        
        # 削除実行
        result = user_repository.delete(saved_user.id)
        
        assert result is True
        assert user_repository.find_by_id(saved_user.id) is None
    
    def test_delete_user_not_found(self, user_repository):
        """ユーザー削除（見つからない場合）テスト"""
        result = user_repository.delete(999)
        assert result is False
    
    def test_exists_by_email(self, user_repository):
        """メールアドレス存在チェックテスト"""
        email = Email("test@example.com")
        now = datetime.now()
        
        # 存在しない場合
        assert user_repository.exists_by_email(email) is False
        
        # ユーザーを作成
        user = User(
            id=None,
            email=email,
            name="テストユーザー",
            created_at=now,
            updated_at=now
        )
        user_repository.save(user)
        
        # 存在する場合
        assert user_repository.exists_by_email(email) is True

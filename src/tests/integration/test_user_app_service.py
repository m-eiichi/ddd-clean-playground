"""
ユーザーアプリケーションサービスの結合テスト
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application.dtos.user_dto import UserCreateDTO, UserUpdateDTO
from application.services.user_app_service import UserAppService
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.db.models import Base


class TestUserAppServiceIntegration:
    """ユーザーアプリケーションサービスの結合テスト"""
    
    @pytest.fixture
    def db_session(self):
        """テスト用データベースセッション"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        yield session
        session.close()
    
    @pytest.fixture
    def user_app_service(self, db_session):
        """ユーザーアプリケーションサービス"""
        user_repository = UserRepositoryImpl(db_session)
        return UserAppService(user_repository)
    
    def test_create_user_success(self, user_app_service):
        """ユーザー作成成功テスト"""
        dto = UserCreateDTO(
            email="test@example.com",
            name="テストユーザー"
        )
        
        result = user_app_service.create_user(dto)
        
        assert result.id is not None
        assert result.email == "test@example.com"
        assert result.name == "テストユーザー"
        assert result.created_at is not None
        assert result.updated_at is not None
    
    def test_create_user_with_duplicate_email_raises_error(self, user_app_service):
        """重複メールアドレスでユーザー作成時にエラーが発生するテスト"""
        dto1 = UserCreateDTO(
            email="test@example.com",
            name="テストユーザー1"
        )
        dto2 = UserCreateDTO(
            email="test@example.com",
            name="テストユーザー2"
        )
        
        # 最初のユーザーは作成成功
        user_app_service.create_user(dto1)
        
        # 2番目のユーザーは重複エラー
        with pytest.raises(ValueError, match="このメールアドレスは既に使用されています"):
            user_app_service.create_user(dto2)
    
    def test_get_user_by_id(self, user_app_service):
        """IDでユーザー取得テスト"""
        dto = UserCreateDTO(
            email="test@example.com",
            name="テストユーザー"
        )
        created_user = user_app_service.create_user(dto)
        
        found_user = user_app_service.get_user_by_id(created_user.id)
        
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == "test@example.com"
        assert found_user.name == "テストユーザー"
    
    def test_get_user_by_id_not_found(self, user_app_service):
        """IDでユーザー取得（見つからない場合）テスト"""
        found_user = user_app_service.get_user_by_id(999)
        assert found_user is None
    
    def test_get_user_by_email(self, user_app_service):
        """メールアドレスでユーザー取得テスト"""
        dto = UserCreateDTO(
            email="test@example.com",
            name="テストユーザー"
        )
        user_app_service.create_user(dto)
        
        found_user = user_app_service.get_user_by_email("test@example.com")
        
        assert found_user is not None
        assert found_user.email == "test@example.com"
        assert found_user.name == "テストユーザー"
    
    def test_get_user_by_email_not_found(self, user_app_service):
        """メールアドレスでユーザー取得（見つからない場合）テスト"""
        found_user = user_app_service.get_user_by_email("notfound@example.com")
        assert found_user is None
    
    def test_update_user_name(self, user_app_service):
        """ユーザー名更新テスト"""
        dto = UserCreateDTO(
            email="test@example.com",
            name="テストユーザー"
        )
        created_user = user_app_service.create_user(dto)
        
        update_dto = UserUpdateDTO(name="更新された名前")
        updated_user = user_app_service.update_user(created_user.id, update_dto)
        
        assert updated_user is not None
        assert updated_user.id == created_user.id
        assert updated_user.name == "更新された名前"
        assert updated_user.email == "test@example.com"
        assert updated_user.updated_at > created_user.updated_at
    
    def test_update_user_email(self, user_app_service):
        """ユーザーメールアドレス更新テスト"""
        dto = UserCreateDTO(
            email="test@example.com",
            name="テストユーザー"
        )
        created_user = user_app_service.create_user(dto)
        
        update_dto = UserUpdateDTO(email="new@example.com")
        updated_user = user_app_service.update_user(created_user.id, update_dto)
        
        assert updated_user is not None
        assert updated_user.id == created_user.id
        assert updated_user.email == "new@example.com"
        assert updated_user.name == "テストユーザー"
        assert updated_user.updated_at > created_user.updated_at
    
    def test_update_user_with_duplicate_email_raises_error(self, user_app_service):
        """重複メールアドレスでユーザー更新時にエラーが発生するテスト"""
        dto1 = UserCreateDTO(
            email="user1@example.com",
            name="ユーザー1"
        )
        dto2 = UserCreateDTO(
            email="user2@example.com",
            name="ユーザー2"
        )
        
        user1 = user_app_service.create_user(dto1)
        user_app_service.create_user(dto2)
        
        # user1のメールアドレスをuser2と同じに変更しようとする
        update_dto = UserUpdateDTO(email="user2@example.com")
        
        with pytest.raises(ValueError, match="このメールアドレスは既に使用されています"):
            user_app_service.update_user(user1.id, update_dto)
    
    def test_update_user_not_found(self, user_app_service):
        """存在しないユーザー更新テスト"""
        update_dto = UserUpdateDTO(name="更新された名前")
        result = user_app_service.update_user(999, update_dto)
        assert result is None
    
    def test_delete_user(self, user_app_service):
        """ユーザー削除テスト"""
        dto = UserCreateDTO(
            email="test@example.com",
            name="テストユーザー"
        )
        created_user = user_app_service.create_user(dto)
        
        # 削除前は存在する
        assert user_app_service.get_user_by_id(created_user.id) is not None
        
        # 削除実行
        result = user_app_service.delete_user(created_user.id)
        
        assert result is True
        assert user_app_service.get_user_by_id(created_user.id) is None
    
    def test_delete_user_not_found(self, user_app_service):
        """存在しないユーザー削除テスト"""
        result = user_app_service.delete_user(999)
        assert result is False
    
    def test_get_users_with_pagination(self, user_app_service):
        """ページネーション付きユーザー一覧取得テスト"""
        # 複数のユーザーを作成
        for i in range(5):
            dto = UserCreateDTO(
                email=f"user{i}@example.com",
                name=f"ユーザー{i}"
            )
            user_app_service.create_user(dto)
        
        # 1ページ目（3件）
        result = user_app_service.get_users(page=1, per_page=3)
        
        assert result.total_count == 5
        assert result.page == 1
        assert result.per_page == 3
        assert len(result.users) == 3
        
        # 2ページ目（2件）
        result = user_app_service.get_users(page=2, per_page=3)
        
        assert result.total_count == 5
        assert result.page == 2
        assert result.per_page == 3
        assert len(result.users) == 2
    
    def test_get_active_users_count(self, user_app_service):
        """アクティブユーザー数取得テスト"""
        # 複数のユーザーを作成
        for i in range(3):
            dto = UserCreateDTO(
                email=f"user{i}@example.com",
                name=f"ユーザー{i}"
            )
            user_app_service.create_user(dto)
        
        count = user_app_service.get_active_users_count()
        assert count == 3
    
    def test_get_users_by_domain(self, user_app_service):
        """ドメイン別ユーザー取得テスト"""
        # 異なるドメインのユーザーを作成
        dto1 = UserCreateDTO(email="user1@example.com", name="ユーザー1")
        dto2 = UserCreateDTO(email="user2@example.com", name="ユーザー2")
        dto3 = UserCreateDTO(email="user3@test.com", name="ユーザー3")
        
        user_app_service.create_user(dto1)
        user_app_service.create_user(dto2)
        user_app_service.create_user(dto3)
        
        # example.comドメインのユーザーを取得
        users = user_app_service.get_users_by_domain("example.com")
        
        assert len(users) == 2
        emails = [user.email for user in users]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails
        assert "user3@test.com" not in emails

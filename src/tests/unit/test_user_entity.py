"""
ユーザーエンティティの単体テスト
"""
import pytest
from datetime import datetime
from domain.models.user import User
from domain.value_objects.email import Email


class TestUserEntity:
    """ユーザーエンティティのテスト"""
    
    def test_create_user_success(self):
        """ユーザー作成成功テスト"""
        email = Email("test@example.com")
        now = datetime.now()
        
        user = User(
            id=1,
            email=email,
            name="テストユーザー",
            created_at=now,
            updated_at=now
        )
        
        assert user.id == 1
        assert user.email == email
        assert user.name == "テストユーザー"
        assert user.created_at == now
        assert user.updated_at == now
    
    def test_create_user_with_empty_name_raises_error(self):
        """空の名前でユーザー作成時にエラーが発生するテスト"""
        email = Email("test@example.com")
        now = datetime.now()
        
        with pytest.raises(ValueError, match="ユーザー名は必須です"):
            User(
                id=1,
                email=email,
                name="",
                created_at=now,
                updated_at=now
            )
    
    def test_create_user_with_long_name_raises_error(self):
        """長すぎる名前でユーザー作成時にエラーが発生するテスト"""
        email = Email("test@example.com")
        now = datetime.now()
        long_name = "a" * 101
        
        with pytest.raises(ValueError, match="ユーザー名は100文字以内で入力してください"):
            User(
                id=1,
                email=email,
                name=long_name,
                created_at=now,
                updated_at=now
            )
    
    def test_change_name_success(self):
        """ユーザー名変更成功テスト"""
        email = Email("test@example.com")
        now = datetime.now()
        
        user = User(
            id=1,
            email=email,
            name="テストユーザー",
            created_at=now,
            updated_at=now
        )
        
        new_name = "新しい名前"
        user.change_name(new_name)
        
        assert user.name == new_name
        assert user.updated_at > now
    
    def test_change_name_with_empty_name_raises_error(self):
        """空の名前でユーザー名変更時にエラーが発生するテスト"""
        email = Email("test@example.com")
        now = datetime.now()
        
        user = User(
            id=1,
            email=email,
            name="テストユーザー",
            created_at=now,
            updated_at=now
        )
        
        with pytest.raises(ValueError, match="ユーザー名は必須です"):
            user.change_name("")
    
    def test_change_email_success(self):
        """メールアドレス変更成功テスト"""
        email = Email("test@example.com")
        new_email = Email("new@example.com")
        now = datetime.now()
        
        user = User(
            id=1,
            email=email,
            name="テストユーザー",
            created_at=now,
            updated_at=now
        )
        
        user.change_email(new_email)
        
        assert user.email == new_email
        assert user.updated_at > now
    
    def test_is_active_returns_true(self):
        """is_activeメソッドがTrueを返すテスト"""
        email = Email("test@example.com")
        now = datetime.now()
        
        user = User(
            id=1,
            email=email,
            name="テストユーザー",
            created_at=now,
            updated_at=now
        )
        
        assert user.is_active() is True

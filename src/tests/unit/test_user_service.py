"""
ユーザードメインサービスの単体テスト
"""
import pytest
from unittest.mock import Mock
from domain.models.user import User
from domain.value_objects.email import Email
from domain.services.user_service import UserService


class TestUserService:
    """ユーザードメインサービスのテスト"""
    
    def setup_method(self):
        """テスト前のセットアップ"""
        self.mock_repository = Mock()
        self.user_service = UserService(self.mock_repository)
    
    def test_is_email_available_when_email_not_exists(self):
        """メールアドレスが存在しない場合のテスト"""
        email = Email("test@example.com")
        self.mock_repository.find_by_email.return_value = None
        
        result = self.user_service.is_email_available(email)
        
        assert result is True
        self.mock_repository.find_by_email.assert_called_once_with(email)
    
    def test_is_email_available_when_email_exists(self):
        """メールアドレスが存在する場合のテスト"""
        email = Email("test@example.com")
        mock_user = Mock()
        self.mock_repository.find_by_email.return_value = mock_user
        
        result = self.user_service.is_email_available(email)
        
        assert result is False
        self.mock_repository.find_by_email.assert_called_once_with(email)
    
    def test_can_change_email_when_same_email(self):
        """同じメールアドレスへの変更の場合のテスト"""
        email = Email("test@example.com")
        user = Mock()
        user.email = email
        
        result = self.user_service.can_change_email(user, email)
        
        assert result is True
        self.mock_repository.find_by_email.assert_not_called()
    
    def test_can_change_email_when_new_email_available(self):
        """新しいメールアドレスが利用可能な場合のテスト"""
        old_email = Email("old@example.com")
        new_email = Email("new@example.com")
        user = Mock()
        user.email = old_email
        self.mock_repository.find_by_email.return_value = None
        
        result = self.user_service.can_change_email(user, new_email)
        
        assert result is True
        self.mock_repository.find_by_email.assert_called_once_with(new_email)
    
    def test_can_change_email_when_new_email_not_available(self):
        """新しいメールアドレスが利用不可能な場合のテスト"""
        old_email = Email("old@example.com")
        new_email = Email("new@example.com")
        user = Mock()
        user.email = old_email
        mock_existing_user = Mock()
        self.mock_repository.find_by_email.return_value = mock_existing_user
        
        result = self.user_service.can_change_email(user, new_email)
        
        assert result is False
        self.mock_repository.find_by_email.assert_called_once_with(new_email)
    
    def test_get_active_users_count(self):
        """アクティブユーザー数の取得テスト"""
        mock_user1 = Mock()
        mock_user1.is_active.return_value = True
        mock_user2 = Mock()
        mock_user2.is_active.return_value = False
        mock_user3 = Mock()
        mock_user3.is_active.return_value = True
        
        self.mock_repository.find_all.return_value = [mock_user1, mock_user2, mock_user3]
        
        result = self.user_service.get_active_users_count()
        
        assert result == 2
        self.mock_repository.find_all.assert_called_once()
    
    def test_get_users_by_domain(self):
        """ドメイン別ユーザー取得テスト"""
        mock_user1 = Mock()
        mock_user1.email.value = "user1@example.com"
        mock_user2 = Mock()
        mock_user2.email.value = "user2@test.com"
        mock_user3 = Mock()
        mock_user3.email.value = "user3@example.com"
        
        self.mock_repository.find_all.return_value = [mock_user1, mock_user2, mock_user3]
        
        result = self.user_service.get_users_by_domain("example.com")
        
        assert len(result) == 2
        assert mock_user1 in result
        assert mock_user3 in result
        assert mock_user2 not in result
        self.mock_repository.find_all.assert_called_once()

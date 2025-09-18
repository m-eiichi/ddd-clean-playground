"""
メールアドレス値オブジェクトの単体テスト
"""
import pytest
from domain.value_objects.email import Email


class TestEmailValueObject:
    """メールアドレス値オブジェクトのテスト"""
    
    def test_create_email_success(self):
        """メールアドレス作成成功テスト"""
        email = Email("test@example.com")
        assert email.value == "test@example.com"
    
    def test_create_email_with_empty_value_raises_error(self):
        """空の値でメールアドレス作成時にエラーが発生するテスト"""
        with pytest.raises(ValueError, match="メールアドレスは必須です"):
            Email("")
    
    def test_create_email_with_invalid_format_raises_error(self):
        """無効な形式でメールアドレス作成時にエラーが発生するテスト"""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test.example.com",
            "test@.com",
            "test@example.",
        ]
        
        for invalid_email in invalid_emails:
            with pytest.raises(ValueError, match="有効なメールアドレス形式ではありません"):
                Email(invalid_email)
    
    def test_create_email_with_long_value_raises_error(self):
        """長すぎるメールアドレスで作成時にエラーが発生するテスト"""
        long_email = "a" * 250 + "@example.com"
        
        with pytest.raises(ValueError, match="メールアドレスは254文字以内で入力してください"):
            Email(long_email)
    
    def test_email_equality(self):
        """メールアドレスの等価性テスト"""
        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        email3 = Email("other@example.com")
        
        assert email1 == email2
        assert email1 != email3
        assert email1 != "test@example.com"  # 文字列とは等しくない
    
    def test_email_hash(self):
        """メールアドレスのハッシュテスト"""
        email1 = Email("test@example.com")
        email2 = Email("test@example.com")
        email3 = Email("other@example.com")
        
        assert hash(email1) == hash(email2)
        assert hash(email1) != hash(email3)
    
    def test_email_string_representation(self):
        """メールアドレスの文字列表現テスト"""
        email = Email("test@example.com")
        assert str(email) == "test@example.com"

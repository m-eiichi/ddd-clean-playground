"""
ユーザーリポジトリインターフェース
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.user import User
from domain.value_objects.email import Email


class UserRepository(ABC):
    """ユーザーリポジトリインターフェース"""
    
    @abstractmethod
    def save(self, user: User) -> User:
        """ユーザーを保存する"""
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """IDでユーザーを検索する"""
        pass
    
    @abstractmethod
    def find_by_email(self, email: Email) -> Optional[User]:
        """メールアドレスでユーザーを検索する"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[User]:
        """すべてのユーザーを取得する"""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """ユーザーを削除する"""
        pass
    
    @abstractmethod
    def exists_by_email(self, email: Email) -> bool:
        """メールアドレスが存在するかチェックする"""
        pass

"""
ユーザードメインサービス
複雑なビジネスルールを実装
"""
from typing import List
from domain.models.user import User
from domain.value_objects.email import Email
from domain.repositories.user_repository import UserRepository


class UserService:
    """ユーザードメインサービス"""
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    def is_email_available(self, email: Email) -> bool:
        """メールアドレスが利用可能かどうかを確認する"""
        existing_user = self._user_repository.find_by_email(email)
        return existing_user is None
    
    def can_change_email(self, user: User, new_email: Email) -> bool:
        """ユーザーがメールアドレスを変更できるかどうかを判定する"""
        # 同じメールアドレスの場合は変更可能
        if user.email == new_email:
            return True
        
        # 他のユーザーが使用していないかチェック
        return self.is_email_available(new_email)
    
    def get_active_users_count(self) -> int:
        """アクティブなユーザー数を取得する"""
        all_users = self._user_repository.find_all()
        active_users = [user for user in all_users if user.is_active()]
        return len(active_users)
    
    def get_users_by_domain(self, domain: str) -> List[User]:
        """指定されたドメインのユーザーを取得する"""
        all_users = self._user_repository.find_all()
        return [
            user for user in all_users 
            if user.email.value.endswith(f"@{domain}")
        ]

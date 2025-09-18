"""
ユーザーエンティティ
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from domain.value_objects.email import Email


@dataclass
class User:
    """ユーザーエンティティ"""
    
    id: Optional[int]
    email: Email
    name: str
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """バリデーション"""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("ユーザー名は必須です")
        
        if len(self.name) > 100:
            raise ValueError("ユーザー名は100文字以内で入力してください")
    
    def change_name(self, new_name: str) -> None:
        """ユーザー名を変更する"""
        if not new_name or len(new_name.strip()) == 0:
            raise ValueError("ユーザー名は必須です")
        
        if len(new_name) > 100:
            raise ValueError("ユーザー名は100文字以内で入力してください")
        
        self.name = new_name
        self.updated_at = datetime.now()
    
    def change_email(self, new_email: Email) -> None:
        """メールアドレスを変更する"""
        self.email = new_email
        self.updated_at = datetime.now()
    
    def is_active(self) -> bool:
        """ユーザーがアクティブかどうかを判定する"""
        # ビジネスルールに基づく判定ロジック
        return True

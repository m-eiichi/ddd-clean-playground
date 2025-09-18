"""
メールアドレス値オブジェクト
"""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """メールアドレス値オブジェクト"""
    
    value: str
    
    def __post_init__(self):
        """バリデーション"""
        if not self.value:
            raise ValueError("メールアドレスは必須です")
        
        # 基本的なメールアドレス形式チェック
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.value):
            raise ValueError("有効なメールアドレス形式ではありません")
        
        if len(self.value) > 254:
            raise ValueError("メールアドレスは254文字以内で入力してください")
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Email):
            return False
        return self.value == other.value
    
    def __hash__(self) -> int:
        return hash(self.value)

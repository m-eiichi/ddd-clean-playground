"""
ユーザーDTO
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserCreateDTO:
    """ユーザー作成用DTO"""
    email: str
    name: str


@dataclass
class UserUpdateDTO:
    """ユーザー更新用DTO"""
    name: Optional[str] = None
    email: Optional[str] = None


@dataclass
class UserResponseDTO:
    """ユーザー応答用DTO"""
    id: int
    email: str
    name: str
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_domain(cls, user) -> 'UserResponseDTO':
        """ドメインモデルからDTOを作成"""
        return cls(
            id=user.id,
            email=str(user.email),
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )


@dataclass
class UserListResponseDTO:
    """ユーザー一覧応答用DTO"""
    users: list[UserResponseDTO]
    total_count: int
    page: int
    per_page: int

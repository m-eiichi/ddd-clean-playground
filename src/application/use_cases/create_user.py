"""
ユーザー作成ユースケース
"""
from datetime import datetime
from typing import Optional
from domain.models.user import User
from domain.value_objects.email import Email
from domain.repositories.user_repository import UserRepository
from domain.services.user_service import UserService
from application.dtos.user_dto import UserCreateDTO, UserResponseDTO


class CreateUserUseCase:
    """ユーザー作成ユースケース"""
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
        self._user_service = UserService(user_repository)
    
    def execute(self, dto: UserCreateDTO) -> UserResponseDTO:
        """ユーザーを作成する"""
        # メールアドレス値オブジェクトを作成
        email = Email(dto.email)
        
        # メールアドレスの重複チェック
        if not self._user_service.is_email_available(email):
            raise ValueError("このメールアドレスは既に使用されています")
        
        # ユーザーエンティティを作成
        now = datetime.now()
        user = User(
            id=None,  # 新規作成時はNone
            email=email,
            name=dto.name,
            created_at=now,
            updated_at=now
        )
        
        # ユーザーを保存
        saved_user = self._user_repository.save(user)
        
        # DTOに変換して返す
        return UserResponseDTO.from_domain(saved_user)

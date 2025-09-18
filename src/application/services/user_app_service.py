"""
ユーザーアプリケーションサービス
複数のユースケースを組み合わせて複雑な処理を実装
"""
from typing import List, Optional
from domain.models.user import User
from domain.value_objects.email import Email
from domain.repositories.user_repository import UserRepository
from domain.services.user_service import UserService
from application.dtos.user_dto import (
    UserCreateDTO, 
    UserUpdateDTO, 
    UserResponseDTO,
    UserListResponseDTO
)
from application.use_cases.create_user import CreateUserUseCase


class UserAppService:
    """ユーザーアプリケーションサービス"""
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
        self._user_service = UserService(user_repository)
        self._create_user_use_case = CreateUserUseCase(user_repository)
    
    def create_user(self, dto: UserCreateDTO) -> UserResponseDTO:
        """ユーザーを作成する"""
        return self._create_user_use_case.execute(dto)
    
    def get_user_by_id(self, user_id: int) -> Optional[UserResponseDTO]:
        """IDでユーザーを取得する"""
        user = self._user_repository.find_by_id(user_id)
        if user is None:
            return None
        return UserResponseDTO.from_domain(user)
    
    def get_user_by_email(self, email: str) -> Optional[UserResponseDTO]:
        """メールアドレスでユーザーを取得する"""
        email_vo = Email(email)
        user = self._user_repository.find_by_email(email_vo)
        if user is None:
            return None
        return UserResponseDTO.from_domain(user)
    
    def update_user(self, user_id: int, dto: UserUpdateDTO) -> Optional[UserResponseDTO]:
        """ユーザーを更新する"""
        user = self._user_repository.find_by_id(user_id)
        if user is None:
            return None
        
        # 名前の更新
        if dto.name is not None:
            user.change_name(dto.name)
        
        # メールアドレスの更新
        if dto.email is not None:
            new_email = Email(dto.email)
            if not self._user_service.can_change_email(user, new_email):
                raise ValueError("このメールアドレスは既に使用されています")
            user.change_email(new_email)
        
        # 保存
        updated_user = self._user_repository.save(user)
        return UserResponseDTO.from_domain(updated_user)
    
    def delete_user(self, user_id: int) -> bool:
        """ユーザーを削除する"""
        return self._user_repository.delete(user_id)
    
    def get_users(self, page: int = 1, per_page: int = 10) -> UserListResponseDTO:
        """ユーザー一覧を取得する"""
        all_users = self._user_repository.find_all()
        total_count = len(all_users)
        
        # ページネーション
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_users = all_users[start_index:end_index]
        
        # DTOに変換
        user_dtos = [UserResponseDTO.from_domain(user) for user in paginated_users]
        
        return UserListResponseDTO(
            users=user_dtos,
            total_count=total_count,
            page=page,
            per_page=per_page
        )
    
    def get_active_users_count(self) -> int:
        """アクティブなユーザー数を取得する"""
        return self._user_service.get_active_users_count()
    
    def get_users_by_domain(self, domain: str) -> List[UserResponseDTO]:
        """指定されたドメインのユーザーを取得する"""
        users = self._user_service.get_users_by_domain(domain)
        return [UserResponseDTO.from_domain(user) for user in users]

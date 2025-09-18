"""
ユーザーAPI
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from application.dtos.user_dto import (
    UserCreateDTO, 
    UserUpdateDTO, 
    UserResponseDTO,
    UserListResponseDTO
)
from application.services.user_app_service import UserAppService
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.db.session import get_db
from infrastructure.external_services.mail_service import MailService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_app_service(db: Session = Depends(get_db)) -> UserAppService:
    """ユーザーアプリケーションサービスの依存性注入"""
    user_repository = UserRepositoryImpl(db)
    return UserAppService(user_repository)


@router.post("/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreateDTO,
    user_service: UserAppService = Depends(get_user_app_service)
):
    """ユーザーを作成する"""
    try:
        user = user_service.create_user(user_data)
        
        # ウェルカムメールを送信
        mail_service = MailService()
        mail_service.send_welcome_email(user_data.email, user_data.name)
        
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="内部サーバーエラー")


@router.get("/{user_id}", response_model=UserResponseDTO)
def get_user(
    user_id: int,
    user_service: UserAppService = Depends(get_user_app_service)
):
    """IDでユーザーを取得する"""
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ユーザーが見つかりません")
    return user


@router.get("/email/{email}", response_model=UserResponseDTO)
def get_user_by_email(
    email: str,
    user_service: UserAppService = Depends(get_user_app_service)
):
    """メールアドレスでユーザーを取得する"""
    user = user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ユーザーが見つかりません")
    return user


@router.put("/{user_id}", response_model=UserResponseDTO)
def update_user(
    user_id: int,
    user_data: UserUpdateDTO,
    user_service: UserAppService = Depends(get_user_app_service)
):
    """ユーザーを更新する"""
    try:
        user = user_service.update_user(user_id, user_data)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ユーザーが見つかりません")
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    user_service: UserAppService = Depends(get_user_app_service)
):
    """ユーザーを削除する"""
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ユーザーが見つかりません")


@router.get("/", response_model=UserListResponseDTO)
def get_users(
    page: int = 1,
    per_page: int = 10,
    user_service: UserAppService = Depends(get_user_app_service)
):
    """ユーザー一覧を取得する"""
    if page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ページ番号は1以上である必要があります")
    if per_page < 1 or per_page > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="1ページあたりの件数は1-100の範囲で指定してください")
    
    return user_service.get_users(page, per_page)


@router.get("/stats/active-count")
def get_active_users_count(
    user_service: UserAppService = Depends(get_user_app_service)
):
    """アクティブなユーザー数を取得する"""
    count = user_service.get_active_users_count()
    return {"active_users_count": count}


@router.get("/domain/{domain}", response_model=List[UserResponseDTO])
def get_users_by_domain(
    domain: str,
    user_service: UserAppService = Depends(get_user_app_service)
):
    """指定されたドメインのユーザーを取得する"""
    return user_service.get_users_by_domain(domain)

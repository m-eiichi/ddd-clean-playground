"""
ユーザーリポジトリ実装
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.user import User
from domain.value_objects.email import Email
from domain.repositories.user_repository import UserRepository
from infrastructure.db.models import UserModel


class UserRepositoryImpl(UserRepository):
    """ユーザーリポジトリ実装"""
    
    def __init__(self, db_session: Session):
        self._db_session = db_session
    
    def save(self, user: User) -> User:
        """ユーザーを保存する"""
        if user.id is None:
            # 新規作成
            user_model = UserModel(
                email=str(user.email),
                name=user.name,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            self._db_session.add(user_model)
            self._db_session.flush()  # IDを取得するためにflush
            user.id = user_model.id
        else:
            # 更新
            user_model = self._db_session.query(UserModel).filter(UserModel.id == user.id).first()
            if user_model:
                user_model.email = str(user.email)
                user_model.name = user.name
                user_model.updated_at = user.updated_at
        
        self._db_session.commit()
        return user
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        """IDでユーザーを検索する"""
        user_model = self._db_session.query(UserModel).filter(UserModel.id == user_id).first()
        if user_model is None:
            return None
        
        return self._model_to_entity(user_model)
    
    def find_by_email(self, email: Email) -> Optional[User]:
        """メールアドレスでユーザーを検索する"""
        user_model = self._db_session.query(UserModel).filter(UserModel.email == str(email)).first()
        if user_model is None:
            return None
        
        return self._model_to_entity(user_model)
    
    def find_all(self) -> List[User]:
        """すべてのユーザーを取得する"""
        user_models = self._db_session.query(UserModel).all()
        return [self._model_to_entity(model) for model in user_models]
    
    def delete(self, user_id: int) -> bool:
        """ユーザーを削除する"""
        user_model = self._db_session.query(UserModel).filter(UserModel.id == user_id).first()
        if user_model is None:
            return False
        
        self._db_session.delete(user_model)
        self._db_session.commit()
        return True
    
    def exists_by_email(self, email: Email) -> bool:
        """メールアドレスが存在するかチェックする"""
        count = self._db_session.query(UserModel).filter(UserModel.email == str(email)).count()
        return count > 0
    
    def _model_to_entity(self, model: UserModel) -> User:
        """ORMモデルをドメインエンティティに変換"""
        return User(
            id=model.id,
            email=Email(model.email),
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

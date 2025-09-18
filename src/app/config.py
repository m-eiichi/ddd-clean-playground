"""
アプリケーション設定
"""
import os
from typing import Optional


class Settings:
    """アプリケーション設定クラス"""
    
    # データベース設定
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # API設定
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DDD Clean Architecture Playground"
    
    # セキュリティ設定
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 外部サービス設定
    MAIL_SERVER: Optional[str] = os.getenv("MAIL_SERVER")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USERNAME: Optional[str] = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: Optional[str] = os.getenv("MAIL_PASSWORD")
    
    # 開発環境設定
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


settings = Settings()

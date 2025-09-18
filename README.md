## フォルダ構成

```
src/
├─ app/                     # アプリケーション全体
│  ├─ __init__.py
│  ├─ main.py               # エントリーポイント（FastAPIやFlaskなど）
│  └─ config.py             # 設定
│
├─ domain/                  # ドメイン層（ビジネスルール）
│  ├─ __init__.py
│  ├─ models/               # エンティティ
│  │   ├─ __init__.py
│  │   └─ user.py
│  ├─ value_objects/        # 値オブジェクト
│  │   ├─ __init__.py
│  │   └─ email.py
│  ├─ services/             # ドメインサービス（複雑なビジネスルール）
│  │   ├─ __init__.py
│  │   └─ user_service.py
│  └─ repositories/         # リポジトリインターフェース
│      ├─ __init__.py
│      └─ user_repository.py
│
├─ application/             # アプリケーション層（ユースケース）
│  ├─ __init__.py
│  ├─ dtos/                 # 入出力用のデータ転送オブジェクト
│  │   ├─ __init__.py
│  │   └─ user_dto.py
│  ├─ use_cases/
│  │   ├─ __init__.py
│  │   └─ create_user.py
│  └─ services/             # アプリケーションサービス（ドメインサービスを呼ぶ）
│      ├─ __init__.py
│      └─ user_app_service.py
│
├─ infrastructure/          # インフラ層（外部との接続）
│  ├─ __init__.py
│  ├─ db/
│  │   ├─ __init__.py
│  │   ├─ models.py         # ORMモデル(SQLAlchemyなど)
│  │   └─ session.py        # DB接続設定
│  ├─ repositories/         # ドメインリポジトリの実装
│  │   ├─ __init__.py
│  │   └─ user_repository_impl.py
│  └─ external_services/    # メール送信や外部APIなど
│      ├─ __init__.py
│      └─ mail_service.py
│
├─ interfaces/              # プレゼンテーション層（UI / API）
│  ├─ __init__.py
│  ├─ api/                  # HTTP API（FastAPIやFlask）
│  │   ├─ __init__.py
│  │   └─ user_api.py
│  └─ cli/                  # CLI用のインターフェース
│      ├─ __init__.py
│      └─ user_cli.py
│
├─ tests/                   # テスト
│  ├─ unit/                 # 単体テスト
│  └─ integration/          # 結合テスト
│
├─ requirements.txt
└─ README.md
```

## 起動方法
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
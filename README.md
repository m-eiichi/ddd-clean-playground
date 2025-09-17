## フォルダ構成

```
my-app/
├─ .devcontainer/              # VSCode Dev Container 設定
│   ├─ devcontainer.json
│   └─ Dockerfile
├─ src/
│   ├─ app/
│   │   ├─ main.py             # エントリーポイント (FastAPI起動)
│   │   ├─ adapters/           # DB, 外部APIの実装 (Infrastructure)
│   │   ├─ core/               # ドメイン層 (Entities, UseCases)
│   │   ├─ interfaces/         # Controller, Presenter, GraphQLなど
│   │   └─ schemas/            # Pydanticモデル (DTO)
│   └─ tests/
│       └─ ...                 # pytest テスト
├─ pyproject.toml              # Poetry で依存管理
└─ README.md
```

## 起動方法
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
FROM python:3.11-slim

# 必要なライブラリ
RUN apt-get update && apt-get install -y \
    build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

# Poetry インストール
RUN pip install poetry

WORKDIR /workspace

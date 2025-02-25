FROM python:3.11.8-bullseye

WORKDIR /workspace/

# poetryのインストール先の指定
ENV POETRY_HOME=/opt/poetry

# poetryインストール
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    # シンボリックによるpathへのpoetryコマンドの追加
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    # 仮想環境を作成しない設定(コンテナ前提のため，仮想環境を作らない)
    poetry config virtualenvs.create false

# pyproject.tomlをコピー
COPY  pyproject.toml ./

# パッケージのインストール
RUN poetry install

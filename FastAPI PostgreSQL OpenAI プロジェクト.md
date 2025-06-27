# FastAPI PostgreSQL OpenAI プロジェクト

FastAPIを使用してPostgreSQLデータベースに接続し、OpenAI APIを統合したバックエンドプロジェクトです。

## 機能

- **ユーザー管理API**: ユーザーの作成、取得、更新、削除
- **投稿管理API**: 投稿の作成、取得、更新、削除
- **AI応答API**: OpenAI APIを使用したテキスト生成とデータベース保存

## 技術スタック

- **FastAPI**: 高性能なPython Webフレームワーク
- **PostgreSQL**: リレーショナルデータベース
- **SQLAlchemy**: Python ORM
- **OpenAI API**: AI テキスト生成
- **Docker**: コンテナ化

## プロジェクト構造

```
fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPIアプリケーション
│   ├── schemas.py           # Pydanticスキーマ
│   └── routers/
│       ├── __init__.py
│       ├── users.py         # ユーザー管理API
│       ├── posts.py         # 投稿管理API
│       └── ai_responses.py  # AI応答API
├── database/
│   ├── __init__.py
│   ├── database.py          # データベース接続設定
│   └── models.py            # SQLAlchemyモデル
├── services/
│   ├── __init__.py
│   └── openai_service.py    # OpenAI APIサービス
├── requirements.txt         # Python依存関係
├── Dockerfile              # Dockerイメージ設定
├── docker-compose.yml      # Docker Compose設定
└── .env                    # 環境変数
```

## セットアップ

### 1. 環境変数の設定

`.env`ファイルを編集して、OpenAI APIキーを設定してください：

```bash
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### 2. Dockerでの起動

```bash
# プロジェクトディレクトリに移動
cd fastapi_project

# Docker Composeでサービスを起動
docker-compose up --build
```

### 3. APIの確認

- **API ドキュメント**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **ヘルスチェック**: http://localhost:8000/health

## API エンドポイント

### ユーザー管理 (`/api/v1/users`)

- `POST /api/v1/users/` - ユーザー作成
- `GET /api/v1/users/` - ユーザー一覧取得
- `GET /api/v1/users/{user_id}` - 特定ユーザー取得
- `PUT /api/v1/users/{user_id}` - ユーザー更新
- `DELETE /api/v1/users/{user_id}` - ユーザー削除

### 投稿管理 (`/api/v1/posts`)

- `POST /api/v1/posts/` - 投稿作成
- `GET /api/v1/posts/` - 投稿一覧取得
- `GET /api/v1/posts/{post_id}` - 特定投稿取得
- `PUT /api/v1/posts/{post_id}` - 投稿更新
- `DELETE /api/v1/posts/{post_id}` - 投稿削除
- `GET /api/v1/posts/user/{user_id}` - ユーザー別投稿取得

### AI応答 (`/api/v1/ai`)

- `POST /api/v1/ai/generate` - AI応答生成（OpenAI API使用）
- `GET /api/v1/ai/` - AI応答一覧取得
- `GET /api/v1/ai/{response_id}` - 特定AI応答取得
- `GET /api/v1/ai/user/{user_id}` - ユーザー別AI応答取得
- `DELETE /api/v1/ai/{response_id}` - AI応答削除

## 使用例

### 1. ユーザー作成

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "full_name": "Test User"
     }'
```

### 2. AI応答生成

```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate?user_id=1" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "こんにちは、今日はいい天気ですね。"
     }'
```

## データベーススキーマ

### Users テーブル
- `id`: 主キー
- `username`: ユーザー名（ユニーク）
- `email`: メールアドレス（ユニーク）
- `full_name`: フルネーム
- `is_active`: アクティブフラグ
- `created_at`, `updated_at`: タイムスタンプ

### Posts テーブル
- `id`: 主キー
- `title`: タイトル
- `content`: 内容
- `author_id`: 作成者ID（外部キー）
- `is_published`: 公開フラグ
- `created_at`, `updated_at`: タイムスタンプ

### AI Responses テーブル
- `id`: 主キー
- `user_id`: ユーザーID（外部キー）
- `prompt`: 入力プロンプト
- `response`: AI応答
- `model`: 使用モデル
- `tokens_used`: 使用トークン数
- `created_at`: タイムスタンプ

## 開発

### ローカル開発環境

```bash
# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 依存関係インストール
pip install -r requirements.txt

# 開発サーバー起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 注意事項

- OpenAI APIキーが必要です
- PostgreSQLデータベースが必要です
- 本番環境では適切なセキュリティ設定を行ってください


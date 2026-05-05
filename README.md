# SkillLog API

SkillLog API は、日々の学習内容・学習時間・使用教材・振り返りを記録できる認証付き学習ログAPIです。

FastAPI を用いて、ユーザー登録、ログイン、JWT認証、カテゴリ管理、学習ログCRUD、検索、学習時間集計を実装しています。  
Docker Compose により、FastAPIアプリとPostgreSQLをまとめて起動できます。

---

## 作成目的

このアプリは、FastAPIを使ったバックエンド開発とAPI認証の理解を深めるために作成しました。

主な目的は以下です。

- REST APIの設計・実装を学ぶ
- JWT認証の流れを理解する
- ユーザーごとにデータを分離する設計を学ぶ
- SQLAlchemyでDB操作を行う
- PostgreSQLとDocker Composeを使った開発環境を経験する
- GitHubで見せられるバックエンド成果物を作る

---

## 使用技術

| 技術 | 用途 |
|---|---|
| Python | メイン言語 |
| FastAPI | APIフレームワーク |
| Uvicorn | ASGIサーバー |
| SQLAlchemy | ORM |
| PostgreSQL | Docker環境で使用するDB |
| SQLite | ローカル直接起動時の簡易DB |
| Pydantic | バリデーション |
| PyJWT | JWTの作成・検証 |
| pwdlib[argon2] | パスワードハッシュ化 |
| Docker | コンテナ化 |
| Docker Compose | APIとDBの同時起動 |

---

## 主な機能

### 認証機能

- ユーザー登録
- ログイン
- JWTアクセストークン発行
- ログイン中ユーザー情報取得
- パスワードハッシュ化

### カテゴリ機能

- カテゴリ作成
- カテゴリ一覧取得
- カテゴリ詳細取得
- カテゴリ更新
- カテゴリ削除

### 学習ログ機能

- 学習ログ作成
- 学習ログ一覧取得
- 学習ログ詳細取得
- 学習ログ更新
- 学習ログ削除

### 検索機能

学習ログは以下の条件で検索できます。

- 開始日
- 終了日
- カテゴリID
- キーワード
- 最小学習時間
- 最大学習時間

### 集計機能

- 総学習時間
- 月別学習時間
- カテゴリ別学習時間
- 期間指定集計

---

## 認証方式

このAPIでは、以下の方式で認証を行います。

```text
OAuth2 Password Bearer + JWT
```

ログインに成功すると、以下のようなアクセストークンが返されます。

```json
{
  "access_token": "xxxxx.yyyyy.zzzzz",
  "token_type": "bearer"
}
```

認証が必要なAPIでは、以下の形式でトークンを送信します。

```http
Authorization: Bearer <access_token>
```

JWTには、ユーザーIDを表す `sub` と有効期限 `exp` を含めています。  
パスワードやハッシュ化済みパスワードはJWTに含めません。

---

## API一覧

### Auth

| メソッド | エンドポイント | 内容 | 認証 |
|---|---|---|---|
| POST | `/auth/register` | ユーザー登録 | 不要 |
| POST | `/auth/login` | ログイン・JWT発行 | 不要 |

### Users

| メソッド | エンドポイント | 内容 | 認証 |
|---|---|---|---|
| GET | `/users/me` | ログイン中ユーザー情報取得 | 必要 |

### Categories

| メソッド | エンドポイント | 内容 | 認証 |
|---|---|---|---|
| POST | `/categories` | カテゴリ作成 | 必要 |
| GET | `/categories` | 自分のカテゴリ一覧取得 | 必要 |
| GET | `/categories/{category_id}` | カテゴリ詳細取得 | 必要 |
| PATCH | `/categories/{category_id}` | カテゴリ更新 | 必要 |
| DELETE | `/categories/{category_id}` | カテゴリ削除 | 必要 |

### Study Logs

| メソッド | エンドポイント | 内容 | 認証 |
|---|---|---|---|
| POST | `/study-logs` | 学習ログ作成 | 必要 |
| GET | `/study-logs` | 自分の学習ログ一覧取得・検索 | 必要 |
| GET | `/study-logs/{log_id}` | 学習ログ詳細取得 | 必要 |
| PATCH | `/study-logs/{log_id}` | 学習ログ更新 | 必要 |
| DELETE | `/study-logs/{log_id}` | 学習ログ削除 | 必要 |

### Stats

| メソッド | エンドポイント | 内容 | 認証 |
|---|---|---|---|
| GET | `/stats/total` | 総学習時間取得 | 必要 |
| GET | `/stats/monthly` | 月別学習時間取得 | 必要 |
| GET | `/stats/by-category` | カテゴリ別学習時間取得 | 必要 |
| GET | `/stats/summary` | 期間指定集計 | 必要 |

---

## 学習ログ検索パラメータ

`GET /study-logs` では、以下のクエリパラメータを指定できます。

| パラメータ | 型 | 内容 |
|---|---|---|
| `start_date` | date | 指定日以降のログを取得 |
| `end_date` | date | 指定日以前のログを取得 |
| `category_id` | int | 指定カテゴリのログを取得 |
| `keyword` | string | タイトル・教材・メモ・振り返りから検索 |
| `min_minutes` | int | 指定分数以上のログを取得 |
| `max_minutes` | int | 指定分数以下のログを取得 |

例：

```http
GET /study-logs?start_date=2026-05-01&end_date=2026-05-31
```

```http
GET /study-logs?keyword=FastAPI&min_minutes=60
```

---

## DB設計

このアプリでは、主に以下の3つのテーブルを使用しています。

- `users`
- `categories`
- `study_logs`

### users

| カラム | 内容 |
|---|---|
| `id` | ユーザーID |
| `username` | ユーザー名 |
| `email` | メールアドレス |
| `hashed_password` | ハッシュ化済みパスワード |
| `is_active` | 有効ユーザーか |
| `created_at` | 作成日時 |
| `updated_at` | 更新日時 |

### categories

| カラム | 内容 |
|---|---|
| `id` | カテゴリID |
| `name` | カテゴリ名 |
| `description` | カテゴリ説明 |
| `owner_id` | 作成者ユーザーID |
| `created_at` | 作成日時 |
| `updated_at` | 更新日時 |

### study_logs

| カラム | 内容 |
|---|---|
| `id` | 学習ログID |
| `owner_id` | 所有者ユーザーID |
| `category_id` | カテゴリID |
| `study_date` | 学習日 |
| `title` | 学習タイトル |
| `minutes` | 学習時間 |
| `resource` | 使用教材 |
| `resource_url` | 教材URL |
| `note` | 学習内容メモ |
| `reflection` | 振り返り |
| `understanding_level` | 理解度 |
| `created_at` | 作成日時 |
| `updated_at` | 更新日時 |

### テーブル関係

```text
users 1 --- * categories
users 1 --- * study_logs
categories 1 --- * study_logs
```

- 1人のユーザーは複数のカテゴリを持つ
- 1人のユーザーは複数の学習ログを持つ
- 1つのカテゴリには複数の学習ログが紐づく

---

## Dockerでの起動方法

### 1. リポジトリをクローン

```bash
git clone https://github.com/sora1204/skilllog-api.git
cd skilllog-api
```

### 2. 環境変数ファイルを作成

Windows PowerShellの場合：

```powershell
Copy-Item .env.example .env
```

macOS / Linux の場合：

```bash
cp .env.example .env
```

### 3. Docker Composeで起動

```bash
docker compose up --build
```

### 4. テーブル作成

別のターミナルで以下を実行します。

```bash
docker compose exec api python -m scripts.create_tables
```

成功すると以下のように表示されます。

```text
Tables created successfully.
```

### 5. APIドキュメントを開く

```text
http://localhost:8000/docs
```

---

## ローカル直接起動

Dockerを使わずにローカルで起動する場合は、SQLiteを使用します。

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m scripts.create_tables
uvicorn app.main:app --reload --reload-dir app
```

Swagger UI：

```text
http://127.0.0.1:8000/docs
```

---

## 環境変数

`.env.example` の例です。

```env
DATABASE_URL=postgresql+psycopg://skilllog_user:skilllog_password@db:5432/skilllog_db
SECRET_KEY=change-this-secret-key-later-please-use-env-file
ACCESS_TOKEN_EXPIRE_MINUTES=60

POSTGRES_USER=skilllog_user
POSTGRES_PASSWORD=skilllog_password
POSTGRES_DB=skilllog_db
```

`.env` はGitHubにpushしません。

---

## 動作確認の流れ

Swagger UIで以下の順に確認できます。

1. `POST /auth/register` でユーザー登録
2. 右上の Authorize でログイン
3. `GET /users/me` でログイン中ユーザー確認
4. `POST /categories` でカテゴリ作成
5. `POST /study-logs` で学習ログ作成
6. `GET /study-logs` で一覧取得
7. `GET /stats/total` で総学習時間取得
8. `GET /stats/by-category` でカテゴリ別集計

---

## 工夫した点

### パスワードを平文保存しない

登録時に受け取ったパスワードは、`pwdlib[argon2]` を使ってハッシュ化してから保存しています。

DBには `password` ではなく、`hashed_password` のみを保存します。

### JWT認証を実装

ログイン成功時にJWTを発行し、認証が必要なAPIでは `Authorization: Bearer <token>` を検証しています。

### ユーザーごとにデータを分離

カテゴリや学習ログには `owner_id` を持たせています。

取得・更新・削除時には、必ずログイン中ユーザーのIDで絞り込んでいます。

```text
owner_id == current_user.id
```

これにより、他人のデータを操作できないようにしています。

### 自分のカテゴリだけを学習ログに紐づける

学習ログ作成時・更新時には、指定された `category_id` がログイン中ユーザーのカテゴリかどうかを確認しています。

これにより、他人のカテゴリIDを指定して学習ログを作ることを防いでいます。

### PATCHによる部分更新

学習ログ更新では、送られてきた項目だけ更新するようにしています。

Pydanticの `model_dump(exclude_unset=True)` を使い、未送信の項目が `None` で上書きされないようにしています。

### 検索・集計APIを実装

単なるCRUDではなく、学習ログを日付・カテゴリ・キーワード・学習時間で検索できます。

また、総学習時間、月別学習時間、カテゴリ別学習時間、期間指定集計も取得できます。

### Docker Compose対応

FastAPIアプリとPostgreSQLをDocker Composeでまとめて起動できるようにしています。

---

## 今後の改善

今後追加したい機能は以下です。

- Alembicによるマイグレーション管理
- pytestによるAPIテスト
- GitHub Actionsによる自動テスト
- Render / Railway などへのデプロイ
- Reactフロントエンド
- 学習目標機能
- 学習カレンダー機能
- CSVエクスポート
- リフレッシュトークン対応

---

## 補足

このアプリは、FastAPIによる認証付きAPI開発を学ぶためのポートフォリオです。

Djangoのテンプレートアプリとは異なり、HTMLを返すのではなく、JSONを返すAPIとして設計しています。

そのため、Reactなどのフロントエンド、モバイルアプリ、外部サービスから利用できる構成になっています。

---

## テスト実行方法

このプロジェクトでは、`pytest` を使ってAPIの動作確認を行っています。

主に以下の内容をテストしています。

- ユーザー登録
- ログイン
- JWT認証
- `/users/me` の認証確認
- カテゴリCRUD
- 学習ログCRUD
- 他人のデータを取得できないこと
- 学習時間集計API

### ローカルでテストを実行する場合

```powershell
pytest
```

詳細表示で実行する場合：

```powershell
pytest -v
```

### Docker環境でテストを実行する場合

```powershell
docker compose exec api pytest
```

テストでは、本番用DBではなく、テスト専用のSQLiteインメモリDBを使用しています。  
そのため、既存のPostgreSQLデータには影響しません。

---
今後の改善
- Alembicによるマイグレーション管理
- GitHub Actionsによる自動テスト
- Render / Railway などへのデプロイ
- Reactフロントエンドの追加
- 学習目標機能
- 学習カレンダー機能
# presentation-reaction-app

発表中にリアルタイムで反応を送受信できるWebアプリケーション

## 概要

発表者が作成したプレゼンテーションに対して、視聴者がリアクション（👍❤️😂😮）を送信できます。リアクション数は1秒ごとに自動更新されます。

## 技術スタック

### フロントエンド
- React + TypeScript
- Vite
- Material-UI (MUI)
- React Router

### バックエンド
- Python
- Django
- PostgreSQL

### デプロイ
- フロントエンド: Render (Static Site)
- バックエンド: Render (Web Service)
- データベース: Render (PostgreSQL)

## 主な機能

- **プレゼンテーション作成**: タイトルと説明を入力して新しいプレゼンテーションを作成
- **リアクション送信**: 4種類のリアクションボタンから選択して送信
- **リアルタイム更新**: 1秒ごとのポーリングで最新のリアクション数を表示
- **URL共有**: プレゼンテーションページのURLを共有して視聴者を招待

## デプロイURL

- フロントエンド: https://presentation-reaction-app.onrender.com
- バックエンドAPI: https://presentation-reaction-api.onrender.com

## ローカル開発

### バックエンド

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### フロントエンド

```bash
cd frontend
npm install
npm run dev
```

## API エンドポイント

- `POST /presentations/create/` - プレゼンテーション作成
- `GET /presentations/{id}/` - プレゼンテーション取得
- `POST /presentations/{id}/reactions/` - リアクション送信

## ライセンス

MIT

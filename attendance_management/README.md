# 勤怠管理システム

## 概要

この Django ベースの勤怠管理システムは、従業員の出勤・退勤を簡単に記録・管理できるウェブアプリケーションです。リアルタイムの勤務時間追跡、ユーザー認証、勤務記録の表示機能を提供します。

## 機能

- ユーザー認証システム
- リアルタイムの出勤・退勤打刻
- 勤務時間の自動計算
- 月次勤務記録の表示
- レスポンシブなユーザーインターフェイス

## 技術スタック

- バックエンド: Django
- フロントエンド: HTML、CSS、JavaScript、Bootstrap
- データベース: SQLite
- API: Django REST Framework

## 必要条件

- Python 3.8+
- pip
- 仮想環境（venv 推奨）

## インストール手順

1. リポジトリをクローン

```bash
git clone https://github.com/your-username/attendance-management.git
cd attendance-management
```

2. 仮想環境を作成・有効化

```bash
python -m venv venv
source venv/bin/activate  # Linuxの場合
venv\Scripts\activate  # Windowsの場合
```

3. 依存関係をインストール

```bash
pip install -r requirements.txt
```

4. データベースを設定

```bash
python manage.py migrate
```

5. スーパーユーザーを作成

```bash
python manage.py createsuperuser
```

6. 開発サーバーを起動

```bash
python manage.py runserver
```

## 使用方法

1. ブラウザで `http://localhost:8000` にアクセス
2. 作成したスーパーユーザーでログイン
3. ダッシュボードで出勤・退勤ボタンを使用

## セキュリティ

- Django 組み込みの認証システムを使用
- CSRF トークンによる保護
- ユーザー別の勤務記録アクセス制限

## カスタマイズ

- `settings.py` で詳細な設定が可能
- スタイルは `static/attendance/css/` で調整可能

## ライセンス

未定義

## 貢献

プルリクエストは歓迎します。大きな変更を行う場合は、まず issue で議論してください。

## 注意事項

- 本番環境では `SECRET_KEY` を必ず変更してください
- 適切なデータベース（PostgreSQL など）への移行を検討してください

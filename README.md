
---

# Mission Matrix

Django + Python で作る「アーカイブ付き TODO リスト / コマンドー風演出」ポートフォリオプロジェクト。

---

## 技術スタック

* Python 3.12
* Django 5.2.5
* HTML (テンプレート)
* セッション管理
* 開発環境: Windows11 + WSL(Ubuntu)

---

## 環境構築手順

### 1. リポジトリをクローン

```bash
git clone https://github.com/ShigeoYugawa/mission_matrix.git
cd mission_matrix
```

### 2. 仮想環境作成

```bash
python3 -m venv venv
source venv/bin/activate  # Linux / macOS
```

### 3. 必要パッケージのインストール

```bash
pip install --upgrade pip
pip install django==5.2.5
pip install mypy django-stubs
```

※ 必要に応じて `requirements.txt` を作成して以下でまとめてインストール可能です：

```bash
pip install -r requirements.txt
```

### 4. Django プロジェクト・アプリ作成（既存プロジェクトの場合は不要）

```bash
# 新規作成の場合
django-admin startproject mission_matrix .
python manage.py startapp complete_colonel
```

### 5. データベースマイグレーション

```bash
python manage.py migrate
```

### 6. 開発用サーバー起動

```bash
python manage.py runserver
```

ブラウザで `http://127.0.0.1:8000/` を開く。

---

## 型チェック (mypy) 設定

mypy を導入して型チェックを行う。

### 1. mypy.ini の例

```ini
[mypy]
python_version = 3.12
warn_unused_configs = True
ignore_missing_imports = True
strict = True

[mypy.plugins.django-stubs]
django_settings_module = "mission_matrix.settings"
```

### 2. 型チェック実行

```bash
mypy complete_colonel
```

* `django-stubs` を使うことで Django モデルやクラスベースビューなども型チェック可能

---

## 使用方法

* 通常モード / コマンドー風モードを切替可能（views.py 内の `COMMANDO_MODE` フラグ）
* 任務（タスク）を追加・完了・アーカイブ・復活・削除可能
* コマンドー風モードではベネットのセリフが表示される

---

## 注意点

* SQLite データベース (`db.sqlite3`) は `.gitignore` で除外済み
* 仮想環境やキャッシュも Git に含めない
* 日本語フォントのドット文字には対応していない

---



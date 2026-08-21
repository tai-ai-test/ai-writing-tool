# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## これは何か

Streamlit と Gemini API で構築された個人用（単一ユーザー・認証やDBなし）のAIライティングツールです。ブログ下書き作成、メール返信、要約、校正、タイトル生成、文体変換といった複数のライティング支援ツールを1つのマルチページアプリにまとめています。

## 技術スタック

- Python
- Streamlit（マルチページアプリ機構）
- Gemini API（`google-genai` SDK）
- python-dotenv（`.env` 読み込み）

バージョン指定は `requirements.txt` を参照（`streamlit>=1.38.0`, `google-genai>=0.3.0`, `python-dotenv>=1.0.1`）。

## ディレクトリ構成

```
app.py                          # エントリーポイント（ランディングページ）
common/
  gemini_utils.py                # Gemini API呼び出しの共通処理
  ui.py                          # サイドバー共通UI
pages/
  1_📝_ブログ記事作成.py
  2_📧_メール返信作成.py
  3_📄_文章要約.py
  4_✅_文章校正.py
  5_💡_タイトル生成.py
  6_🎭_文体変換.py
requirements.txt
.env.example                     # コピーして .env を作成し GEMINI_API_KEY を設定
```

## コマンド

セットアップ（Windows）:
```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

アプリの起動:
```
.venv\Scripts\python.exe -m streamlit run app.py
```
（PowerShellのスクリプト実行がブロックされる場合があるため、venvをactivateするより `.venv\Scripts\python.exe` を直接呼び出す方法を優先してください。）

全Pythonファイルの構文チェック（このリポジトリにテストスイートはありません）:
```
.venv\Scripts\python.exe -m py_compile app.py common/gemini_utils.py common/ui.py pages/*.py
```

APIキーは `.env`（`.env.example` をコピーし、キー名は `GEMINI_API_KEY`）で設定するか、実行時にアプリのサイドバーから入力します — サイドバー入力は `st.session_state` にのみ保持され、永続化されません。

## アーキテクチャ

- `app.py` がエントリーポイント（ランディングページ）です。それ以外の全ページは `pages/` 配下にあり、Streamlitのマルチページ機構がファイル名（`<順番>_<絵文字>_<名前>.py`）からサイドバーのナビゲーションを自動生成します。新しいツールを追加する場合はこのディレクトリにファイルを追加するだけでよく、手動のルーティングは不要です。
- `common/gemini_utils.py` がGemini APIとの唯一の接点です（`google-genai` SDK、`google.genai.Client` を使用）。`get_api_key()` はまず `st.session_state["gemini_api_key"]` からキーを解決し、なければ環境変数 `GEMINI_API_KEY` にフォールバックします。`generate_text()` が各ページから補完を得るために呼ぶ唯一の関数で、キーが未設定の場合は `RuntimeError` を送出します。
- `common/ui.py` は `render_sidebar_settings()`（APIキー入力とモデル選択をレンダリングし、各ページの先頭で呼ばれ、選択中のモデル名を返す）と `show_api_key_warning()`（生成前に呼ぶ。キー未設定なら警告を表示して `True` を返すので、呼び出し側は `st.stop()` すべき）を提供します。
- 各ツールページは同じパターンに従います: `render_sidebar_settings()` を呼ぶ → `st.text_input`/`st.text_area`/`st.selectbox` でフォームを構築する → 送信時に `show_api_key_warning()` を呼んでから `st.spinner` 内で `generate_text(prompt, model=model)` を呼ぶ → 結果を `st.session_state`（例: `st.session_state["blog_result"]`）にキャッシュしてリラン後も保持する。新しいツールを追加する際は、別の構造を考案するのではなくこのパターンに従ってください。
- データベース、認証、Streamlit自体を超えるバックエンドサーバーは存在しません — 状態はすべてブラウザセッションの間だけ `st.session_state` に保持されます。

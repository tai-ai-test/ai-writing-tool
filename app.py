import streamlit as st

from common.ui import render_sidebar_settings

st.set_page_config(page_title="AIライティングツール", page_icon="✍️", layout="wide")

render_sidebar_settings()

st.title("✍️ AIライティングツール")
st.write("Gemini APIを使った個人用のライティング支援ツール集です。左のサイドバーからページを選んでください。")

st.markdown(
    """
### 収録ツール

| ツール | できること |
|---|---|
| 📝 ブログ記事作成 | テーマ・キーワードからブログ記事の下書きを生成 |
| 📧 メール返信作成 | 受信メールの内容から返信文を生成 |
| 📄 文章要約 | 長文を指定した長さ・形式で要約 |
| ✅ 文章校正 | 誤字脱字・文法・表現をチェックして修正案を提示 |
| 💡 タイトル生成 | 記事内容から複数のタイトル案を生成 |
| 🎭 文体変換 | 文章の口調・トーンを変換（丁寧語⇔カジュアルなど） |

### 使い方
1. サイドバーで Gemini APIキーを入力（`.env` に `GEMINI_API_KEY` を設定していれば不要）
2. 使いたいツールのページを開く
3. 必要な情報を入力して生成ボタンを押す
"""
)

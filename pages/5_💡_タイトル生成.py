import streamlit as st

from common.gemini_utils import generate_text
from common.ui import render_sidebar_settings, show_api_key_warning

st.set_page_config(page_title="タイトル生成", page_icon="💡", layout="wide")
model = render_sidebar_settings()

st.title("💡 タイトル生成")
st.caption("記事の内容やテーマから、複数のタイトル案を生成します。")

text = st.text_area("記事の内容・要約（または本文）", height=250, placeholder="ここに記事の内容やテーマを入力してください")

col1, col2 = st.columns(2)
with col1:
    num = st.slider("生成するタイトル数", min_value=3, max_value=15, value=8)
with col2:
    style = st.selectbox("タイトルの傾向", ["バランス型", "SEO意識（検索されやすいワード重視）", "煽り・クリック誘引型", "シンプル・簡潔"])

if st.button("タイトルを生成", type="primary", disabled=not text):
    if show_api_key_warning():
        st.stop()

    prompt = f"""以下の内容に基づいて、記事タイトル案を{num}個、日本語で生成してください。

【傾向】{style}

番号付きリストで出力してください。

【内容】
{text}"""

    with st.spinner("生成中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["title_result"] = result
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

if "title_result" in st.session_state:
    st.divider()
    st.markdown(st.session_state["title_result"])

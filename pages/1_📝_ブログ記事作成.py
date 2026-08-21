import streamlit as st

from common.gemini_utils import generate_text
from common.ui import render_sidebar_settings, show_api_key_warning

st.set_page_config(page_title="ブログ記事作成", page_icon="📝", layout="wide")
model = render_sidebar_settings()

st.title("📝 ブログ記事作成")
st.caption("テーマやキーワードからブログ記事の下書きを生成します。")

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("記事のテーマ", placeholder="例: 在宅ワークの生産性を上げるコツ")
    keywords = st.text_input("含めたいキーワード（任意・カンマ区切り）", placeholder="例: 集中力, タイムブロッキング")
    tone = st.selectbox("文体", ["丁寧・解説調", "カジュアル", "熱意のあるセールス調", "専門的・硬め"])
with col2:
    length = st.select_slider("文章量", options=["短め（400字程度）", "標準（800字程度）", "長め（1500字程度）"], value="標準（800字程度）")
    audience = st.text_input("想定読者（任意）", placeholder="例: 20代の会社員")
    extra = st.text_area("その他の指示（任意）", placeholder="例: 見出しを3つに分けて、最後にまとめを入れてほしい")

if st.button("記事を生成", type="primary", disabled=not topic):
    if show_api_key_warning():
        st.stop()

    prompt = f"""以下の条件でブログ記事の下書きを日本語で作成してください。

テーマ: {topic}
キーワード: {keywords or "指定なし"}
文体: {tone}
文章量: {length}
想定読者: {audience or "指定なし"}
その他の指示: {extra or "なし"}

見出し（##）を使って構成し、読みやすい記事にしてください。"""

    with st.spinner("生成中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["blog_result"] = result
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

if "blog_result" in st.session_state:
    st.divider()
    st.markdown(st.session_state["blog_result"])
    st.download_button("記事をダウンロード", st.session_state["blog_result"], file_name="blog_draft.md")

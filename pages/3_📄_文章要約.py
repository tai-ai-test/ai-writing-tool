import streamlit as st

from common.gemini_utils import generate_text
from common.ui import render_sidebar_settings, show_api_key_warning

st.set_page_config(page_title="文章要約", page_icon="📄", layout="wide")
model = render_sidebar_settings()

st.title("📄 文章要約")
st.caption("長文を指定した長さ・形式で要約します。")

text = st.text_area("要約したい文章", height=300, placeholder="ここに文章を貼り付けてください")

col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("要約形式", ["文章形式", "箇条書き", "1行での要点まとめ"])
with col2:
    length = st.select_slider("要約の長さ", options=["短め", "標準", "長め"], value="標準")

if st.button("要約する", type="primary", disabled=not text):
    if show_api_key_warning():
        st.stop()

    prompt = f"""以下の文章を日本語で要約してください。

【形式】{style}
【長さ】{length}

【文章】
{text}"""

    with st.spinner("生成中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["summary_result"] = result
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

if "summary_result" in st.session_state:
    st.divider()
    st.markdown(st.session_state["summary_result"])

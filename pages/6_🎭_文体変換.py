import streamlit as st

from common.gemini_utils import generate_text
from common.ui import render_sidebar_settings, show_api_key_warning

st.set_page_config(page_title="文体変換", page_icon="🎭", layout="wide")
model = render_sidebar_settings()

st.title("🎭 文体変換")
st.caption("文章の口調やトーンを変換します（例: 丁寧語⇔カジュアル）。")

text = st.text_area("変換したい文章", height=250, placeholder="ここに文章を貼り付けてください")

target_style = st.selectbox(
    "変換先のスタイル",
    [
        "敬語・ビジネス丁寧語",
        "カジュアル・friendly",
        "丁寧語だが親しみやすい",
        "簡潔・端的",
        "SNS向け（絵文字少なめ）",
        "子供にもわかる言葉",
    ],
)
extra = st.text_input("その他の指示（任意）", placeholder="例: 一人称は「私」にする")

if st.button("変換する", type="primary", disabled=not text):
    if show_api_key_warning():
        st.stop()

    prompt = f"""以下の文章を、意味内容は変えずに文体だけを変換してください。

【変換先スタイル】{target_style}
【その他の指示】{extra or "なし"}

【文章】
{text}"""

    with st.spinner("生成中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["style_result"] = result
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

if "style_result" in st.session_state:
    st.divider()
    st.markdown(st.session_state["style_result"])

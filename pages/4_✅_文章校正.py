import streamlit as st

from common.gemini_utils import generate_text
from common.ui import render_sidebar_settings, show_api_key_warning

st.set_page_config(page_title="文章校正", page_icon="✅", layout="wide")
model = render_sidebar_settings()

st.title("✅ 文章校正")
st.caption("誤字脱字・文法・表現をチェックし、修正案を提示します。")

text = st.text_area("校正したい文章", height=300, placeholder="ここに文章を貼り付けてください")
strictness = st.select_slider(
    "校正の強さ", options=["最小限（誤字脱字のみ）", "標準（文法・表現も含む）", "がっつり（より自然な表現に書き換え）"], value="標準（文法・表現も含む）"
)

if st.button("校正する", type="primary", disabled=not text):
    if show_api_key_warning():
        st.stop()

    prompt = f"""以下の日本語の文章を校正してください。

【校正の強さ】{strictness}

出力は次の2部構成にしてください。
1. 修正版の全文
2. 主な修正点の一覧（箇条書きで「修正前 → 修正後：理由」の形式）

【文章】
{text}"""

    with st.spinner("生成中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["proof_result"] = result
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

if "proof_result" in st.session_state:
    st.divider()
    st.markdown(st.session_state["proof_result"])

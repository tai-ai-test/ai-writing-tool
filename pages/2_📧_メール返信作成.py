import streamlit as st

from common.gemini_utils import generate_text
from common.ui import render_sidebar_settings, show_api_key_warning

st.set_page_config(page_title="メール返信作成", page_icon="📧", layout="wide")
model = render_sidebar_settings()

st.title("📧 メール返信作成")
st.caption("受信したメールの内容から返信文の下書きを生成します。")

received_mail = st.text_area("受信したメール本文", height=200, placeholder="ここに届いたメールを貼り付けてください")

col1, col2 = st.columns(2)
with col1:
    intent = st.text_area("返信したい内容の要点", placeholder="例: 日程は来週火曜14時でOK。資料は今週中に送る。")
    tone = st.selectbox("文体", ["ビジネス丁寧語", "ややカジュアル", "フォーマル（社外・目上向け）"])
with col2:
    sender_name = st.text_input("自分の名前（署名用・任意）")
    extra = st.text_area("その他の指示（任意）", placeholder="例: 簡潔に3文程度でまとめて")

if st.button("返信文を生成", type="primary", disabled=not received_mail or not intent):
    if show_api_key_warning():
        st.stop()

    prompt = f"""以下の受信メールに対する返信メールを日本語で作成してください。

【受信メール】
{received_mail}

【返信で伝えたい要点】
{intent}

【文体】
{tone}

【署名】
{sender_name or "指定なし（署名は省略可）"}

【その他の指示】
{extra or "なし"}

件名と本文を分けて出力してください。"""

    with st.spinner("生成中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["mail_result"] = result
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

if "mail_result" in st.session_state:
    st.divider()
    st.markdown(st.session_state["mail_result"])
    st.download_button("返信文をダウンロード", st.session_state["mail_result"], file_name="reply_mail.txt")

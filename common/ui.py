"""ページ共通のサイドバーUIなど。"""
import streamlit as st

from common.gemini_utils import DEFAULT_MODEL, MODEL_OPTIONS, get_api_key


def render_sidebar_settings() -> str:
    """APIキー入力とモデル選択をサイドバーに描画し、選択中モデル名を返す。"""
    with st.sidebar:
        st.header("設定")

        if not get_api_key():
            api_key_input = st.text_input(
                "Gemini APIキー",
                type="password",
                help="環境変数 GEMINI_API_KEY が未設定の場合はここに入力してください。",
                key="gemini_api_key_input",
            )
            if api_key_input:
                st.session_state["gemini_api_key"] = api_key_input
        else:
            st.success("APIキー設定済み")

        model = st.selectbox("使用モデル", MODEL_OPTIONS, index=MODEL_OPTIONS.index(DEFAULT_MODEL))

        st.divider()
        st.caption("個人用 AI ライティングツール")

    return model


def show_api_key_warning() -> bool:
    """APIキー未設定なら警告を表示してTrueを返す。"""
    if not get_api_key():
        st.warning("サイドバーからGemini APIキーを入力してください。")
        return True
    return False

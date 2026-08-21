"""Gemini API 呼び出しの共通ユーティリティ。"""
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

DEFAULT_MODEL = "gemini-3.6-flash"
MODEL_OPTIONS = ["gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.1-pro-preview", "gemini-3.5-flash-lite"]


def get_api_key() -> str | None:
    return st.session_state.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY")


def get_client() -> genai.Client | None:
    api_key = get_api_key()
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def generate_text(
    prompt: str,
    system_instruction: str | None = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
) -> str:
    """Gemini にプロンプトを送り、生成されたテキストを返す。"""
    client = get_client()
    if client is None:
        raise RuntimeError("Gemini APIキーが設定されていません。サイドバーから入力してください。")

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
    )
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    return response.text or ""

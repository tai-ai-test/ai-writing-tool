# AIライティングツール

Streamlit + Gemini API を使った個人用のライティング支援ツール集です。

## 収録ツール
- 📝 ブログ記事作成
- 📧 メール返信作成
- 📄 文章要約
- ✅ 文章校正
- 💡 タイトル生成
- 🎭 文体変換

## セットアップ

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

`.env.example` を `.env` にコピーし、Gemini APIキーを設定してください（未設定でもアプリのサイドバーから入力可能です）。

```
GEMINI_API_KEY=your_api_key_here
```

## 起動

```bash
streamlit run app.py
```

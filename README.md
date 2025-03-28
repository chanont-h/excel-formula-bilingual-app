# Excel Formula Bilingual App

🔍 A bilingual Streamlit app to search and learn Excel formulas (English-Thai).

## Features
- Multi-Keyword Search
- Auto-Suggest Formula Name
- Filter by Category & Difficulty
- Bookmark & Export Tutorials
- Auto-Deploy via GitHub Actions

## Setup

1. Clone this repo
2. Add `.env` file with:
```
OPENAI_API_KEY=your_openai_key
```
3. Run locally:
```
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Auto)
Push a new tag:
```
git tag v1.3.0
git push origin v1.3.0
```
Streamlit Cloud will auto-deploy

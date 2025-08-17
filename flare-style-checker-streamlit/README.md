# Flare Style Checker — Streamlit

Scan **MadCap Flare HTML** for MSTP-style issues and grammar (LanguageTool), review suggestions, accept/reject, and download the cleaned file.

## Features
- Upload a single Flare HTML topic (`.htm`/`.html`)
- Built-in **MSTP rules** (regex-based) — easily extendable in `mstp_rules.py`
- **Grammar checks** via LanguageTool Public API (optional; rate-limited)
- Review suggestions in an editable table (toggle **apply** per change)
- Apply accepted changes and **download cleaned HTML**
- See a **unified diff** preview

## Local run

```bash
# 1) Create and activate a virtual environment (recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install requirements
pip install -r requirements.txt

# 3) Run the Streamlit app
streamlit run streamlit_app.py
```

## Deploy to Streamlit Community Cloud

1. Push this folder to a GitHub repo (e.g., `nikhil/flare-style-checker-streamlit`).
2. Go to https://share.streamlit.io/ → **New app** → select your repo.
3. Set **Main file path**: `streamlit_app.py`
4. Deploy. Done! You'll get a public URL to share.

> Note: Grammar uses the LanguageTool Public API by default through `language_tool_python`. It may be rate-limited. You can disable Grammar in the sidebar or point to a self-hosted LanguageTool server by swapping to `LanguageTool('en-US')` and running the LT server separately.

## Extend MSTP rules
Edit `mstp_rules.py` and add entries:
```py
{
  "id": "MSTP.009",
  "desc": "Your rule description",
  "pattern": re.compile(r"regex", re.IGNORECASE),
  "repl": "replacement",
}
```

## Structure
```
.
├── streamlit_app.py
├── processors.py
├── mstp_rules.py
├── requirements.txt
└── README.md
```

## Flask + React (Alternative)
If you later want a React UI on **GitHub Pages** and an API backend:
- Host React (Vite/CRA) on GitHub Pages.
- Deploy Flask (with your MSTP + grammar logic) on **Render** or **Railway**.
- Expose endpoints like `/api/check` and `/api/apply`. The React app uploads the HTML, renders suggestions, and calls the API to apply changes.
```

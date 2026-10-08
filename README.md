# 📄 ATS Resume Checker

Upload a resume (PDF, DOCX or TXT) and get:

- An overall **ATS score** (0-100) with a breakdown: keywords, formatting, content, impact
- A short assessment and list of strengths
- **Missing keywords** worth adding
- **Prioritized, resume-specific improvements** (High / Medium / Low)
- Optional **job description** input for role-specific keyword matching
- Downloadable JSON report

Built with [Streamlit](https://streamlit.io) and Google's Gemini Flash model.

## Setup

```bash
git clone https://github.com/<your-username>/ats-resume-checker.git
cd ats-resume-checker
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Get a free API key at https://aistudio.google.com/apikey, then provide it in one of these ways:

**Option A - secrets file (recommended)**

Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-key-here"
# GEMINI_MODEL = "gemini-2.5-flash"   # optional override
```

**Option B - environment variable**

```bash
export GEMINI_API_KEY="your-key-here"     # Windows: set GEMINI_API_KEY=your-key-here
```

**Option C** - paste the key into the sidebar when the app runs.

## Run

```bash
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (never commit `secrets.toml`).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app**, pick the repo, branch `main`, main file `app.py`.
4. Open **Advanced settings → Secrets** and paste:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
5. Click **Deploy**.

## Notes and limitations

- The score is an AI estimate of ATS-friendliness, not the output of a real ATS. Treat it as guidance.
- Scanned or image-only PDFs have no extractable text; use a text-based PDF or DOCX.
- Resumes are sent to the Gemini API for analysis. The app does not store them.
- Change the model with the `GEMINI_MODEL` setting if Google retires or updates model names.

## Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI, text extraction and Gemini analysis |
| `requirements.txt` | Python dependencies |
| `README.md` | This file |

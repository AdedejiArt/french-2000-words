# French Quiz App

A web app to quiz yourself on the 2000 most common French words.

## Project structure

```
french-quiz/
├── main.py              # FastAPI app + API routes
├── french_words.json    # All 2000 words extracted from the PDF
├── templates/
│   └── index.html       # Frontend (single page)
├── static/              # Static assets (empty for now)
├── requirements.txt
└── render.yaml          # Render deploy config
```

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open http://localhost:8000

## Deploy on Render

1. Push this folder to a GitHub repo
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repo
4. Render will auto-detect render.yaml and configure everything
5. Hit Deploy — your app will be live in ~2 minutes

## API endpoints

GET  /api/words?start=1&end=20   → words in range (max 100 at a time)
POST /api/check                  → check answer {"num": 1, "answer": "un"}
GET  /                           → the quiz frontend

## Answer checking

- Case-insensitive
- Accent-insensitive (typing "a" matches "à")
- For masculine/feminine words, either form is accepted

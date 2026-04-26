import json
import unicodedata
from pathlib import Path
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI(title="French Quiz API")

# Load words once at startup
DATA_PATH = Path(__file__).parent / "french_words.json"
with open(DATA_PATH, encoding="utf-8") as f:
    ALL_WORDS: list[dict] = json.load(f)

WORDS_BY_NUM: dict[int, dict] = {w["num"]: w for w in ALL_WORDS}


# ── helpers ───────────────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Lowercase, strip accents, keep only letters."""
    text = text.strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text


# ── API routes ────────────────────────────────────────────────────────────────

@app.get("/api/words")
def get_words(
    start: int = Query(1, ge=1, le=2000),
    end: int = Query(10, ge=1, le=2000),
):
    """Return words between start and end (inclusive)."""
    if start > end:
        raise HTTPException(400, "start must be <= end")

    words = [WORDS_BY_NUM[n] for n in range(start, end + 1) if n in WORDS_BY_NUM]
    return JSONResponse([
        {
            "num": w["num"],
            "english": w["english"],
            "french": w["french"],
            "example_fr": w["example_fr"],
            "example_en": w["example_en"],
        }
        for w in words
    ])


class CheckRequest(BaseModel):
    num: int
    answer: str


@app.post("/api/check")
def check_answer(body: CheckRequest):
    """Check a user's answer against all accepted French forms."""
    word = WORDS_BY_NUM.get(body.num)
    if not word:
        raise HTTPException(404, f"Word {body.num} not found")

    accepted = [normalize(f) for f in word["french"]]
    user_tokens = [
        normalize(t)
        for t in body.answer.replace("|", " ").replace("/", " ").replace(",", " ").split()
        if t.strip()
    ]

    correct = any(u in accepted for u in user_tokens)

    return {
        "correct": correct,
        "accepted": word["french"],
        "example_fr": word["example_fr"],
        "example_en": word["example_en"],
    }


# ── Serve frontend ────────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index():
    return (Path(__file__).parent / "templates" / "index.html").read_text(encoding="utf-8")

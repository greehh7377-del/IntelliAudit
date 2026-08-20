from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="IntelliAudit API",
    description="AI-Powered Enterprise Audit, Risk & Fraud Detection Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Paths -----------------------------------------------------------
# This file lives at: backend/app/main.py
# The frontend lives at: frontend/index.html
# So the project root is two levels up from this file.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
INDEX_FILE = FRONTEND_DIR / "index.html"


# ---- Serve the whole website from one page ----------------------------
@app.get("/")
def serve_frontend():
    """Serve the full IntelliAudit dashboard as the homepage."""
    return FileResponse(INDEX_FILE)


# If the frontend folder ever has extra assets (css/js/images), this
# makes them reachable at /static/<filename> automatically.
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "IntelliAudit"}


class Transaction(BaseModel):
    amount: float
    country: str
    failed_attempts: int
    account_age_days: int


@app.post("/audit")
def audit_transaction(transaction: Transaction):
    risk_score = 0
    reasons = []

    if transaction.amount >= 100000:
        risk_score += 40
        reasons.append("Very high transaction amount")

    if transaction.failed_attempts >= 3:
        risk_score += 25
        reasons.append("Multiple failed attempts")

    if transaction.account_age_days < 30:
        risk_score += 20
        reasons.append("New account")

    if transaction.country.lower() not in ["india", "usa", "uk"]:
        risk_score += 15
        reasons.append("Unusual country")

    if risk_score >= 60:
        risk_level = "HIGH"
    elif risk_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons,
    }


@app.get("/dashboard")
def dashboard_redirect():
    """Old dashboard route kept for compatibility -- just serves the same page."""
    return FileResponse(INDEX_FILE)

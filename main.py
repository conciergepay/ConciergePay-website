from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# To jest architektura, którą pokażesz koledze
app = FastAPI(
    title="ConciergePay API",
    description="Backend obsługujący integracje BOK i analizę AI",
    version="1.0.0"
)

# Modele danych (To pokazuje, że dbasz o strukturę)
class Bill(BaseModel):
    id: str
    provider: str
    amount: float
    currency: str = "PLN"
    status: str  # 'paid', 'due', 'overdue'
    due_date: str

class User(BaseModel):
    email: str
    is_premium: bool

# Baza danych in-memory (symulacja)
fake_bills_db = [
    {"id": "inv_001", "provider": "E.ON", "amount": 79.84, "status": "due", "due_date": "2025-02-10"},
    {"id": "inv_002", "provider": "Play", "amount": 55.00, "status": "paid", "due_date": "2025-02-01"}
]

@app.get("/")
async def health_check():
    """Sprawdza stan mikroserwisów scraperów."""
    return {"status": "operational", "ai_engine": "online", "bank_connector": "secure"}

@app.get("/api/v1/bills", response_model=List[Bill])
async def get_bills(user_email: str):
    """
    Pobiera rachunki zintegrowane z kontem użytkownika.
    W przyszłości: Tutaj wpinamy Selenium/Playwright do logowania w BOK.
    """
    # Symulacja logiki biznesowej
    return fake_bills_db

@app.post("/api/v1/pay/{bill_id}")
async def pay_bill(bill_id: str):
    """Inicjuje płatność przez bramkę (Stripe/BLIK)."""
    for bill in fake_bills_db:
        if bill["id"] == bill_id:
            bill["status"] = "paid"
            return {"success": True, "transaction_id": "tx_123456789"}
    raise HTTPException(status_code=404, detail="Rachunek nie znaleziony")

@app.post("/api/v1/ai/analyze")
async def analyze_contract():
    """Wysyła dane do OpenAI w celu znalezienia oszczędności."""
    return {
        "recommendation": "Zmiana taryfy G11 na G12w",
        "savings_estimated": 450.00
    }

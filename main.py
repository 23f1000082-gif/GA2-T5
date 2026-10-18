import hmac

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

EMAIL = "23f1000082@ds.study.iitm.ac.in"
API_KEY = "ak_a39zlv1rxyqwnj8a6imoyunz"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analytics")
def analytics(payload: dict, x_api_key: str | None = Header(default=None)):
    if x_api_key is None or not hmac.compare_digest(x_api_key, API_KEY):
        raise HTTPException(status_code=401, detail="invalid api key")

    events = payload.get("events") or []
    users = set()
    totals = {}
    revenue = 0.0

    for e in events:
        user = e.get("user")
        users.add(user)
        try:
            amount = float(e.get("amount", 0))
        except (TypeError, ValueError):
            amount = 0.0
        if amount > 0:
            revenue += amount
            totals[user] = totals.get(user, 0.0) + amount

    top_user = max(totals, key=totals.get) if totals else None

    return {
        "email": EMAIL,
        "total_events": len(events),
        "unique_users": len(users),
        "revenue": round(revenue, 2),
        "top_user": top_user,
    }


@app.get("/")
def root():
    return {"status": "ok"}

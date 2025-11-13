import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from database import create_document, get_documents, db
from schemas import Tournament as TournamentSchema, Registration as RegistrationSchema

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# -------------------------
# Gaming Tournaments API
# -------------------------

class TournamentOut(BaseModel):
    id: str
    title: str
    game: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    entry_fee_inr: int
    prize_pool_inr: int
    mode: str
    slots: int
    region: Optional[str] = None
    featured: bool = False
    banner_url: Optional[str] = None


def _serialize(doc: dict) -> dict:
    d = {**doc}
    if d.get("_id"):
        d["id"] = str(d.pop("_id"))
    return d


@app.get("/tournaments", response_model=List[TournamentOut])
def list_tournaments():
    try:
        items = get_documents("tournament", {}, limit=None)
        if not items:
            # Seed a few demo tournaments if empty
            seed_data: List[TournamentSchema] = [
                TournamentSchema(
                    title="Valorant Royale Cup",
                    game="Valorant",
                    description="Tier-1 bracket with BO3 finals",
                    start_date=datetime.utcnow(),
                    end_date=None,
                    entry_fee_inr=499,
                    prize_pool_inr=150000,
                    mode="Online",
                    slots=64,
                    region="India",
                    featured=True,
                    banner_url="https://images.unsplash.com/photo-1600861194942-f883de0dfe96?q=80&w=1600&auto=format&fit=crop"
                ),
                TournamentSchema(
                    title="BGMI Clash Series",
                    game="BGMI",
                    description="Squad TPP with live broadcast",
                    start_date=datetime.utcnow(),
                    entry_fee_inr=299,
                    prize_pool_inr=75000,
                    mode="Online",
                    slots=100,
                    region="India",
                    featured=True,
                    banner_url="https://images.unsplash.com/photo-1511512578047-dfb367046420?q=80&w=1600&auto=format&fit=crop"
                ),
                TournamentSchema(
                    title="CS2 Kings Arena",
                    game="Counter-Strike 2",
                    description="5v5 LAN, Bengaluru",
                    start_date=datetime.utcnow(),
                    end_date=None,
                    entry_fee_inr=999,
                    prize_pool_inr=300000,
                    mode="Offline",
                    slots=16,
                    region="Bengaluru",
                    featured=False,
                    banner_url="https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=1600&auto=format&fit=crop"
                )
            ]
            for s in seed_data:
                try:
                    create_document("tournament", s)
                except Exception:
                    pass
            items = get_documents("tournament", {}, limit=None)
        return [TournamentOut(**_serialize(i)) for i in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/register")
def register_user(payload: RegistrationSchema):
    try:
        reg_id = create_document("registration", payload)
        return {"ok": True, "id": reg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

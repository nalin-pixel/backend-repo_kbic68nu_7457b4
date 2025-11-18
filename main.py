import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Subscriber, Message, Event, TimelineEntry

app = FastAPI(title="Carthage Techno Opera API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"name": "Carthage: A Techno Opera", "status": "ok"}


@app.get("/test")
def test_database():
    status = {
        "backend": "running",
        "database": "disconnected",
        "collections": [],
    }
    try:
        if db is None:
            status["database"] = "not_configured"
        else:
            status["database"] = "connected"
            status["collections"] = db.list_collection_names()
    except Exception as e:
        status["database"] = f"error: {str(e)[:100]}"
    return status


# Newsletter subscribe
@app.post("/api/subscribe")
def subscribe(sub: Subscriber):
    try:
        sub_id = create_document("subscriber", sub)
        return {"ok": True, "id": sub_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Contact message
@app.post("/api/contact")
def contact(msg: Message):
    try:
        msg_id = create_document("message", msg)
        return {"ok": True, "id": msg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Events list (for upcoming shows)
@app.get("/api/events", response_model=List[Event])
def list_events(limit: int = 20):
    try:
        docs = get_documents("event", {}, limit=limit)
        # Pydantic conversion
        events: List[Event] = []
        for d in docs:
            # Convert date from string if stored incorrectly
            date_value = d.get("date")
            if isinstance(date_value, str):
                try:
                    date_value = datetime.fromisoformat(date_value)
                except Exception:
                    date_value = datetime.utcnow()
            events.append(Event(
                title=d.get("title", ""),
                date=date_value,
                venue=d.get("venue", ""),
                location=d.get("location", ""),
                url=d.get("url"),
                description=d.get("description"),
            ))
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Timeline content (curated historical entries)
@app.get("/api/timeline", response_model=List[TimelineEntry])
def get_timeline(limit: int = 50):
    try:
        docs = get_documents("timelineentry", {}, limit=limit)
        entries: List[TimelineEntry] = []
        for d in docs:
            entries.append(TimelineEntry(
                year=d.get("year", ""),
                title=d.get("title", ""),
                description=d.get("description", ""),
                tags=d.get("tags"),
            ))
        return entries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

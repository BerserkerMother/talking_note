from fastapi import APIRouter
from fastapi import HTTPException

from service import note_service
from dto import Note

router = APIRouter()

@router.post("/api/v1/notes")
def add_note(item: dict):
    if not item:
        raise HTTPException(status_code=400, detail="Invalid JSON body")
    note = Note(title=item["title"], text=item["text"], userID=item["userID"])
    
from fastapi import Request
from fastapi.responses import JSONResponse

from service import NoteService
from dto import Note


class NoteHandler:
    def __init__(self, ns: NoteService):
        self.ns = ns

    def add_note(self, request: Request) -> JSONResponse:
        data = request.json()
        note = Note(title=data["title"], text=data["text"], userID=data["userID"])
        primary_key = self.ns.insert_note(note=note)
        return JSONResponse({"primary_key": primary_key})

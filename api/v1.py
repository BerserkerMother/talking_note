from fastapi import FastAPI

from handler import NoteHandler
from service import NoteService
from embeddings import VectorDatabase

# TODO: setup config files.

note_db = VectorDatabase()
note_serivce = NoteService(db=note_db)
note_handler = NoteHandler(ns=note_serivce)

app = FastAPI()

# add routes

app.add_route("POST", "/api/v1/note", note_handler.add_note)

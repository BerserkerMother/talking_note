from typing import List

from embeddings import VectorDatabase
from embeddings import get_batch_embedding, get_embedding
from dto import Note, NoteSearchRequest


class NoteService:
    def __init__(self, db: VectorDatabase):
        """_summary_

        Args:
            db (VectorDatabase): _description_
        """
        self.db = db

    def insert_note(self, note: Note):
        text = f"{note.title}\n\n{note.text}"
        embedding = get_embedding(text=text)
        primary_keys = self.db.insert_vectors(user_ids=note.user_id, vectors=embedding)
        return primary_keys[0]

    def insert_notes(self, notes: List[Note]):
        user_ids, texts = [], []
        for note in notes:
            user_ids.append(note.user_id)
            texts.append(f"{note.title}\n\n{note.text}")
        embeddings = get_batch_embedding(batched_text=texts)
        primary_keys = self.db.insert_vectors(user_ids=user_ids, vectors=embeddings)
        return primary_keys

    def search_notes(self, nsr: NoteSearchRequest) -> List[int]:
        user_id = nsr.user_id
        vector = get_embedding(nsr.text)
        result = self.db.search_vectors(user_id=user_id, query_vectors=[vector])
        return [user_id for _, _, user_id in result[0]]


if __name__ == "__main__":
    db = VectorDatabase()
    ns = NoteService(db=db)
    note = Note(
        title="My first test note",
        text="In this we test if we can succesfuly insert note to db",
        userID=3,
    )
    # ns.insert_note(note)
    # print(ns.db.collection.query("user_id == 1", output_fields=["user_id", "vector"]))
    print(ns.search_notes(nsr=NoteSearchRequest(userID=1, text="whatever podcast")))
    print(ns.search_notes(nsr=NoteSearchRequest(userID=1, text="whatever podcast")))
    ns.db.collection.release()

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
        text = nsr.text
        result = self.db.search_vectors(user_id=user_id, query_vectors=[text])
        return [id for id, _ in result[0]]


if __name__ == "__main__":
    db = VectorDatabase()
    ns = NoteService(db=db)
    try:
        ns.db.collection.release()
    except:
        None
    note = Note(
        title="My first test note",
        text="In this we test if we can succesfuly insert note to db",
        userID=0,
    )
    ns.insert_note(note)
    ns.db.collection.create_index(
        field_name="vector",
        index_params={"index_type": "FLAT", "metric_type": "L2", "params": {}},
    )
    ns.db.collection.load()
    print(ns.db.collection.query("user_id == 0", output_fields=["user_id", "vector"]))
    ns.db.collection.release()

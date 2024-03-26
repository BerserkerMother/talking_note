# embeddings/database.py
from pymilvus import (
    Collection,
    CollectionSchema,
    FieldSchema,
    DataType,
    connections,
    utility,
)
from typing import List

from .vectorizer import get_batch_embedding


class VectorDatabase:
    def __init__(self, collection_name="user_notes"):
        self.collection_name = collection_name
        connections.connect()
        self.collection = self._get_or_create_collection()

    def _has_collection(self, collection_name: str) -> bool:
        try:
            return utility.has_collection(collection_name=collection_name)
        except:
            print("error")

    def _get_or_create_collection(self):
        if not self._has_collection(self.collection_name):
            fields = [
                FieldSchema(
                    name="id", dtype=DataType.INT64, is_primary=True, auto_id=True
                ),
                FieldSchema(name="user_id", dtype=DataType.INT64),  # User ID field
                FieldSchema(
                    name="vector", dtype=DataType.FLOAT_VECTOR, dim=1536
                ),  # Adjust 'dim' according to your vector size
            ]
            schema = CollectionSchema(fields, description="User Notes Collection")
            collection = Collection(name=self.collection_name, schema=schema)
            collection.create_index(
                field_name="vector",
                index_params={"index_type": "FLAT", "metric_type": "L2", "params": {}},
            )
        else:
            collection = Collection(name=self.collection_name)
        try:
            collection.release()
        except:
            print("error happened when trying to release collection")
        return collection

    def insert_vectors(self, user_ids, vectors):
        """Insert vectors with associated user IDs into the collection."""
        if isinstance(user_ids, str):
            user_ids = list(user_ids)
        if isinstance(vectors, List) and isinstance(vectors[0], float):
            vectors = list(vectors)
        entities = [
            # Assuming each vector in `vectors` corresponds to a user ID in `user_ids`
            [user_ids],  # User IDs
            [vectors],  # Vectors
        ]
        mr = self.collection.insert(entities)
        return mr.primary_keys

    def search_vectors(self, user_id, query_vectors, top_k=5):
        """Search for similar vectors belonging to a specific user."""
        self.collection.load()
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        # Filtering by user_id
        expr = f"user_id == {user_id}"
        results = self.collection.search(
            data=query_vectors,
            anns_field="vector",
            param=search_params,
            limit=top_k,
            expr=expr,
            output_fields=["id", "user_id"],
        )
        print(results)
        return [
            [(hit.id, hit.distance, hit.entity.user_id) for hit in result]
            for result in results
        ]

    def get_user_ids(self, ids: List[int]) -> List[int]:
        NotImplemented


# Example usage
if __name__ == "__main__":
    db = VectorDatabase()
    # Example data, replace with actual user_ids and vectors
    user_ids = [123]  # User ID associated with each vector
    example_vectors = [[0.1, 0.2, 0.3, ...]]  # Your vectors here
    ids = db.insert_vectors(user_ids, example_vectors)
    print(f"Inserted vector IDs: {ids}")

    # Search for similar vectors for a specific user
    search_results = db.search_vectors(
        user_id=123, query_vectors=example_vectors, top_k=3
    )
    print(f"Search results: {search_results}")

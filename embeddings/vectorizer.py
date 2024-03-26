from typing import List
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from openai import OpenAI

client = OpenAI()


def get_embedding(text: str, model="text-embedding-3-small") -> List[float]:
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def get_batch_embedding(batched_text: List[str]) -> List[List[float]]:
    """Generates embeddings for texts

    Args:
        batched_text (List[str]): _description_

    Returns:
        List[List[float]]: _description_
    """
    vector_list = []
    with ThreadPoolExecutor() as exec:
        futures = []
        for text in batched_text:
            futures.append(
                exec.submit(
                    partial(get_embedding, model="text-embedding-3-small"), text
                )
            )
        for future in futures:
            vector_list.append(future.result())
    return vector_list

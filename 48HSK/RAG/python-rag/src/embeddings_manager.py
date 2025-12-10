from typing import List
import openai
import numpy as np

class EmbeddingsManager:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def create_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        embeddings = []
        for text in texts:
            response = openai.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            embeddings.append(np.array(response.data[0].embedding))
        return embeddings
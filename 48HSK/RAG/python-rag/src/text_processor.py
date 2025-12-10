from typing import List

class TextProcessor:
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size

    def split_into_chunks(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0

        for word in words:
            if current_size + len(word) > self.chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = len(word)
            else:
                current_chunk.append(word)
                current_size += len(word) + 1

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks
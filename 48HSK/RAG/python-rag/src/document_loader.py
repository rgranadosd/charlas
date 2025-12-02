import os
from typing import List

class DocumentLoader:
    def __init__(self, documents_path: str):
        self.documents_path = documents_path

    def load_documents(self) -> List[str]:
        documents = []
        for filename in os.listdir(self.documents_path):
            if filename.endswith('.txt'):
                with open(os.path.join(self.documents_path, filename), 'r') as file:
                    documents.append(file.read())
        return documents
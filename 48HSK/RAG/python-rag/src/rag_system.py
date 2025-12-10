import os
from dotenv import load_dotenv
from typing import List
import openai

from .document_loader import DocumentLoader
from .text_processor import TextProcessor
from .embeddings_manager import EmbeddingsManager
from .retrieval_system import RetrievalSystem

class RAGSystem:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.loader = DocumentLoader('data/documents')
        self.processor = TextProcessor()
        self.embeddings_manager = EmbeddingsManager(self.api_key)

        # Initialize system
        self.initialize_system()

    def initialize_system(self):
        # Load and process documents
        documents = self.loader.load_documents()
        self.chunks = []
        for doc in documents:
            self.chunks.extend(self.processor.split_into_chunks(doc))

        # Create embeddings
        self.embeddings = self.embeddings_manager.create_embeddings(self.chunks)

        # Initialize retrieval system
        self.retrieval_system = RetrievalSystem(self.chunks, self.embeddings)

    def answer_question(self, question: str) -> str:
        # Get question embedding
        question_embedding = self.embeddings_manager.create_embeddings([question])[0]

        # Get relevant chunks
        relevant_chunks = self.retrieval_system.find_similar_chunks(question_embedding)

        # Prepare context
        context = "\n".join([chunk[0] for chunk in relevant_chunks])

        # Create prompt
        prompt = f"""Context: {context}\n\nQuestion: {question}\n\nAnswer:"""

        # Get response from OpenAI
        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Use the provided context to answer the question."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

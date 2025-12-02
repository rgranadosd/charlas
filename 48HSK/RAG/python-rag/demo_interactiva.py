#!/usr/bin/env python3
import os
import sys
import numpy as np
from typing import List
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq

# Color stderr wrapper for warnings - colors huggingface/tokenizers warnings and related lines
class ColoredStderr:
    def __init__(self, original_stderr):
        self.original_stderr = original_stderr
        self.ORANGE = "\033[38;5;208m"
        self.RESET = "\033[0m"
        self.buffer = ""
        self.in_warning_block = False
    
    def write(self, text):
        self.buffer += text
        # Process line by line
        while '\n' in self.buffer:
            line, self.buffer = self.buffer.split('\n', 1)
            # Check if this line starts a warning block
            if 'huggingface/tokenizers' in line:
                self.in_warning_block = True
                colored_line = f"{self.ORANGE}{line}\n{self.RESET}"
                self.original_stderr.write(colored_line)
            # If we're in a warning block, color all lines until we hit an empty line
            elif self.in_warning_block:
                if line.strip() == "":
                    # Empty line ends the warning block
                    self.in_warning_block = False
                    self.original_stderr.write(line + '\n')
                else:
                    # This line is part of the warning block
                    colored_line = f"{self.ORANGE}{line}\n{self.RESET}"
                    self.original_stderr.write(colored_line)
            else:
                # Pass through other stderr messages unchanged
                self.original_stderr.write(line + '\n')
    
    def flush(self):
        # Flush any remaining buffer
        if self.buffer:
            if self.in_warning_block or 'huggingface/tokenizers' in self.buffer:
                colored_text = f"{self.ORANGE}{self.buffer}{self.RESET}"
                self.original_stderr.write(colored_text)
            else:
                self.original_stderr.write(self.buffer)
            self.buffer = ""
        self.original_stderr.flush()

# Redirect stderr to apply orange color to huggingface/tokenizers warnings
sys.stderr = ColoredStderr(sys.stderr)

# Simple ANSI color helpers for nicer CLI output
# Color scheme organized by purpose:
CYAN = "\033[36m"          # Cyan for section titles and headers
YELLOW = "\033[33m"        # Yellow for steps and processes
GREEN = "\033[32m"         # Green for success/completed actions
ORANGE = "\033[38;5;208m"  # Orange for warnings
RED = "\033[31m"           # Red for errors
BLUE = "\033[34m"          # Blue for information/responses
RESET = "\033[0m"


def cyan(msg: str) -> str:
    """Wrap a message so it is printed in cyan (section titles)."""
    return f"{CYAN}{msg}{RESET}"


def yellow(msg: str) -> str:
    """Wrap a message so it is printed in yellow (steps/processes)."""
    return f"{YELLOW}{msg}{RESET}"


def green(msg: str) -> str:
    """Wrap a message so it is printed in green (success/completed)."""
    return f"{GREEN}{msg}{RESET}"


def orange(msg: str) -> str:
    """Wrap a message so it is printed in orange (warnings)."""
    return f"{ORANGE}{msg}{RESET}"


def red(msg: str) -> str:
    """Wrap a message so it is printed in red (errors)."""
    return f"{RED}{msg}{RESET}"


def blue(msg: str) -> str:
    """Wrap a message so it is printed in blue (information/responses)."""
    return f"{BLUE}{msg}{RESET}"


class RAGInteractivaDemo:
    def __init__(self):
        load_dotenv()
        
        # 1. Retrieve your Groq API key
        self.groq_api_key = os.getenv('GROQ-TOKEN')
        
        print(green("Loading local Mistral E5 model (embeddings)..."))
        # 2. Load free local embeddings model
        self.embedding_model = SentenceTransformer('intfloat/multilingual-e5-large')
        print(green("Embedding model loaded successfully."))
        
        # 3. Initialize Groq client
        if self.groq_api_key:
            self.groq_client = Groq(api_key=self.groq_api_key)
            print(green("Groq client initialized successfully."))
        else:
            self.groq_client = None
            print(orange("\nWARNING: 'GROQ-TOKEN' was not found in the .env file"))
            print(orange("   (The final response generation step will not work)\n"))
            
        self.chunks = []
        self.embeddings = []
    
    def mostrar_banner(self):
        print("\n" + cyan("="*80))
        print(cyan(" " * 20 + "INTERACTIVE RAG DEMO (FREE)"))
        print(cyan("="*80))
        print(blue("Technology: Mistral E5 (Local) + Llama 3 (Groq Cloud)"))
        print(blue("\nThis demo will show you step by step how RAG works\n"))
    
    def cargar_texto(self):
        print("\n" + yellow("-"*80))
        print(yellow("STEP 1: LOAD DOCUMENT"))
        print(yellow("-"*80))
        print(blue("\nOptions:"))
        print(blue("1. Use example document (story.txt)"))
        print(blue("2. Paste your own text"))
        print(blue("3. Write a short text now"))
        
        opcion = input("\nChoose an option (1-3): ").strip()
        
        texto = ""
        if opcion == "1":
            ruta = 'data/documents/story.txt'
            if os.path.exists(ruta):
                with open(ruta, 'r') as f:
                    texto = f.read()
                print(green(f"\nDocument loaded: story.txt ({len(texto)} characters)"))
            else:
                print(red(f"\nError: {ruta} does not exist"))
                return ""
        elif opcion == "2":
            print(blue("\nPaste your text (press Enter, then Ctrl+D on Mac/Linux or Ctrl+Z on Windows):"))
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                texto = '\n'.join(lines)
            print(green(f"\nText loaded ({len(texto)} characters)"))
        else:
            print(blue("\nWrite a short text (press Enter twice to finish):"))
            lines = []
            empty_count = 0
            while empty_count < 2:
                line = input()
                if line == "":
                    empty_count += 1
                else:
                    empty_count = 0
                lines.append(line)
            texto = '\n'.join(lines)
            print(green(f"\nText entered ({len(texto)} characters)"))
        
        return texto
    
    def dividir_en_chunks(self, texto: str, chunk_size: int = 500) -> List[str]:
        if not texto: return []
        print("\n" + yellow("-"*80))
        print(yellow("STEP 2: SPLIT INTO CHUNKS"))
        print(yellow("-"*80))
        print(green(f"\nSplitting the text into chunks of ~{chunk_size} characters..."))
        
        palabras = texto.split()
        chunks = []
        chunk_actual = []
        tamaño_actual = 0
        
        for palabra in palabras:
            if tamaño_actual + len(palabra) > chunk_size:
                chunks.append(' '.join(chunk_actual))
                chunk_actual = [palabra]
                tamaño_actual = len(palabra)
            else:
                chunk_actual.append(palabra)
                tamaño_actual += len(palabra) + 1
        
        if chunk_actual:
            chunks.append(' '.join(chunk_actual))
        
        print(green(f"Text split into {len(chunks)} chunks\n"))
        
        for i, chunk in enumerate(chunks, 1):
            preview = chunk[:100] + "..." if len(chunk) > 100 else chunk
            print(blue(f"  Chunk {i}: {preview}"))
        
        return chunks
    
    def crear_embeddings(self, chunks: List[str]) -> List[np.ndarray]:
        if not chunks: return []
        print("\n" + yellow("-"*80))
        print(yellow("STEP 3: CREATE EMBEDDINGS (NUMERIC VECTORS)"))
        print(yellow("-"*80))
        print(green("\nConverting chunks to numbers with Mistral E5 (Local)..."))
        
        # Prefix required for E5
        chunks_con_prefijo = ["passage: " + c for c in chunks]
        
        # Local generation
        embeddings = self.embedding_model.encode(chunks_con_prefijo, normalize_embeddings=True)
        
        print(green(f"{len(embeddings)} embeddings created successfully."))
        return embeddings
    
    def buscar_similares(self, pregunta: str, top_k: int = 3):
        print("\n" + yellow("-"*80))
        print(yellow("STEP 4: FIND RELEVANT CHUNKS"))
        print(yellow("-"*80))
        print(blue(f"\nQuestion: '{pregunta}'"))
        print(green("\nConverting question to embedding (Local)..."))
        
        # Prefix required for questions in E5
        pregunta_embedding = self.embedding_model.encode(["query: " + pregunta], normalize_embeddings=True)[0]
        print(green("Question embedding created"))
        
        print(green("\nCalculating similarity with each chunk..."))
        similitudes = []
        for i, embedding in enumerate(self.embeddings):
            # Dot product (works like cosine similarity because they are normalized)
            similitud = np.dot(pregunta_embedding, embedding)
            similitudes.append((self.chunks[i], similitud, i))
            
            # Only show moderately relevant ones to avoid cluttering the screen
            if similitud > 0.7: 
                print(green(f"  Chunk {i+1}: similarity = {similitud:.4f}"))
        
        similitudes_ordenadas = sorted(similitudes, key=lambda x: x[1], reverse=True)[:top_k]
        
        print(green(f"\nTop {len(similitudes_ordenadas)} most relevant chunks:"))
        for i, (chunk, sim, idx) in enumerate(similitudes_ordenadas, 1):
            preview = chunk[:150] + "..." if len(chunk) > 150 else chunk
            print(blue(f"\n  #{i} (Chunk {idx+1}, Similarity: {sim:.4f}):"))
            print(blue(f"     {preview}"))
        
        return similitudes_ordenadas
    
    def generar_respuesta(self, pregunta: str, contextos: List[tuple]):
        print("\n" + yellow("-"*80))
        print(yellow("STEP 5: GENERATE ANSWER WITH GROQ (Llama 3)"))
        print(yellow("-"*80))
        
        contexto = "\n\n".join([chunk for chunk, _, _ in contextos])
        
        print(yellow("\nSending to Groq Cloud..."))
        print(blue(f"  - Context length: {len(contexto)} characters"))
        print(blue(f"  - Question: {pregunta}"))
        print(yellow("\nGenerating answer..."))
        
        if not self.groq_client:
            return "Error: No connection to Groq (missing token)."

        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant. Use the provided context to answer the question accurately and concisely in English."
                    },
                    {
                        "role": "user", 
                        "content": f"Context:\n{contexto}\n\nQuestion: {pregunta}\n\nAnswer:"
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            
            respuesta = chat_completion.choices[0].message.content
            return respuesta
            
        except Exception as e:
            return f"Error calling Groq: {e}"
    
    def ejecutar_demo(self):
        self.mostrar_banner()
        
        # Step 1: Load text
        texto = self.cargar_texto()
        if not texto: return
        
        input("\nPress Enter to continue...")
        
        # Step 2: Split into chunks
        self.chunks = self.dividir_en_chunks(texto)
        
        input("\nPress Enter to continue...")
        
        # Step 3: Create embeddings
        self.embeddings = self.crear_embeddings(self.chunks)
        
        input("\nPress Enter to continue...")
        
        # Steps 4 and 5: Question loop
        print("\n" + cyan("="*80))
        print(cyan("SYSTEM READY - You can now ask questions"))
        print(cyan("="*80))
        print(blue("\nType 'exit' to finish\n"))
        
        while True:
            print(yellow("-"*80))
            pregunta = input("\nYour question: ").strip()
            
            if pregunta.lower() in ['salir', 'exit', 'quit']:
                print(blue("\nThank you for using the demo!\n"))
                break
            
            if not pregunta:
                continue
            
            # Find relevant chunks
            contextos = self.buscar_similares(pregunta)
            
            if not contextos:
                print(orange("No relevant chunks were found."))
                continue

            # Generate answer
            respuesta = self.generar_respuesta(pregunta, contextos)
            
            print("\n" + cyan("="*80))
            print(cyan("FINAL ANSWER"))
            print(cyan("="*80))
            print(blue(f"\n{respuesta}\n"))


if __name__ == "__main__":
    demo = RAGInteractivaDemo()
    demo.ejecutar_demo()

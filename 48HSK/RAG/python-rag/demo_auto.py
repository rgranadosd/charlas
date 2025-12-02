#!/usr/bin/env python3
import os
import sys
import numpy as np
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
GREEN = "\033[32m"         # Green for success/completed actions (✓)
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

class RAGDemoAutomatica:
    def __init__(self):
        # Load variables from .env file
        load_dotenv()
        
        # Read your exact variable 'GROQ-TOKEN'
        self.groq_api_key = os.getenv('GROQ-TOKEN')
        
        print(green("Loading local Mistral E5 model (embeddings)..."))
        # We use the multilingual E5 model (FREE and LOCAL)
        self.embedding_model = SentenceTransformer('intfloat/multilingual-e5-large')
        print(green("Embedding model loaded successfully."))
        
        # Initialize Groq client with your token
        if self.groq_api_key:
            self.groq_client = Groq(api_key=self.groq_api_key)
            print(green("Groq client initialized successfully (Using GROQ-TOKEN)."))
        else:
            self.groq_client = None
            print(orange("\nIMPORTANT WARNING: The variable 'GROQ-TOKEN' was not found in the .env file"))
            print(orange("   The final chat part will not work without it.\n"))

    def ejecutar(self):
        print(cyan("="*80))
        print(cyan(" "*15 + "RAG DEMO: Mistral E5 (Local) + Llama 3 (Groq Free)"))
        print(cyan("="*80))
        
        # STEP 1: LOAD DOCUMENT
        print("\n" + yellow("-"*80))
        print(yellow("STEP 1: LOAD DOCUMENT"))
        print(yellow("-"*80))
        
        file_path = 'data/documents/story.txt'
        
        if not os.path.exists(file_path):
            print(red(f"\nCRITICAL ERROR: File not found: {file_path}"))
            print(red("Please create the file 'data/documents/story.txt' with some text inside."))
            return

        with open(file_path, 'r') as f:
            texto = f.read()
            
        print(green(f"\nDocument loaded: story.txt"))
        print(green(f"  Size: {len(texto)} characters"))
        print(green(f"\n  First lines of the content:"))
        primeras_lineas = '\n  '.join(texto.split('\n')[:3])
        print(green(f"  {primeras_lineas}"))
        
        # STEP 2: SPLIT INTO CHUNKS
        print("\n" + yellow("-"*80))
        print(yellow("STEP 2: SPLIT INTO CHUNKS"))
        print(yellow("-"*80))
        palabras = texto.split()
        chunks = []
        chunk_actual = []
        chunk_size = 500
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
        
        print(green(f"\nDocument split into {len(chunks)} chunks of ~{chunk_size} characters"))
        
        # STEP 3: CREATE EMBEDDINGS (LOCAL)
        print("\n" + yellow("-"*80))
        print(yellow("STEP 3: CREATE EMBEDDINGS (VECTORS) - LOCAL MODE"))
        print(yellow("-"*80))
        print(green("\nGenerating embeddings with Mistral E5 (Local and free process)..."))
        
        # The prefix "passage: " is necessary for the E5 model to work well
        chunks_con_prefijo = ["passage: " + chunk for chunk in chunks]
        
        # Generate numeric vectors
        embeddings = self.embedding_model.encode(chunks_con_prefijo, normalize_embeddings=True)
        
        print(green(f"{len(embeddings)} vectors have been generated successfully."))
        
        # STEP 4: ASK A QUESTION
        print("\n" + cyan("="*80))
        print(cyan("ASK A QUESTION TO THE SYSTEM"))
        print(cyan("="*80))
        
        pregunta = "What did Rafa have for breakfast?"
        print(blue(f"\nQuestion: '{pregunta}'"))
        
        print("\n" + yellow("-"*80))
        print(yellow("STEP 4: FIND RELEVANT CHUNKS"))
        print(yellow("-"*80))
        
        print(green("\n  1. Converting question to vector..."), end=" ")
        # The prefix "query: " is necessary for questions in E5
        pregunta_embedding = self.embedding_model.encode(["query: " + pregunta], normalize_embeddings=True)[0]
        print(green("Done"))
        
        print(green("\n  2. Comparing similarity with the document:"))
        similitudes = []
        for i, embedding in enumerate(embeddings):
            # Mathematical similarity calculation (dot product)
            similitud = np.dot(pregunta_embedding, embedding)
            similitudes.append((chunks[i], similitud, i))
            
            # Show only if it is relevant to avoid filling the screen
            if similitud > 0.75:
                print(green(f"    Chunk {i+1}: High similarity ({similitud:.4f})"))
        
        # Sort and take the 2 best
        similitudes_ordenadas = sorted(similitudes, key=lambda x: x[1], reverse=True)[:2]
        
        print(green(f"\n  Best chunks selected:"))
        for i, (chunk, sim, idx) in enumerate(similitudes_ordenadas, 1):
            print(green(f"\n    Top #{i} (Chunk {idx+1}):"))
            preview = chunk[:150] + "..." if len(chunk) > 150 else chunk
            print(green(f"    '{preview}'"))
        
        # STEP 5: GENERATE FINAL ANSWER WITH GROQ
        print("\n" + yellow("-"*80))
        print(yellow("STEP 5: GENERATE FINAL ANSWER (USING GROQ)"))
        print(yellow("-"*80))
        
        contexto = "\n\n".join([chunk for chunk, _, _ in similitudes_ordenadas])
        
        if self.groq_client:
            print(yellow("\n  Sending information to Groq (Model Llama-3.3-70b)..."))
            try:
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful and precise assistant. Answer the question based ONLY on the provided context. Answer in English."
                        },
                        {
                            "role": "user",
                            "content": f"Context:\n{contexto}\n\nQuestion: {pregunta}\n\nAnswer:"
                        }
                    ],
                    model="llama-3.3-70b-versatile", # Modelo potente y gratis de Groq
                )
                
                respuesta = chat_completion.choices[0].message.content
                
                print("\n" + cyan("="*80))
                print(cyan("FINAL ANSWER"))
                print(cyan("="*80))
                print(blue(f"\n{respuesta}\n"))
                
            except Exception as e:
                print(red("\nError connecting to Groq:"))
                print(red(f"{e}"))
                print(orange("\n(Check that your GROQ-TOKEN is correct in the .env file)"))
        else:
            print(red("\nThe final answer could not be generated."))
            print(orange("   The variable 'GROQ-TOKEN' is missing in the .env file"))

        print(cyan("="*80))
        print(cyan("END OF DEMO"))
        print(cyan("="*80))

if __name__ == "__main__":
    demo = RAGDemoAutomatica()
    demo.ejecutar()

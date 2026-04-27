#!/usr/bin/env python3
import os
import sys
import time
import numpy as np
from typing import List
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import httpx
import requests
import base64
import urllib3
urllib3.disable_warnings()

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


def get_embedding_model_name() -> str:
    return os.getenv('RAG_EMBEDDING_MODEL', 'intfloat/multilingual-e5-small')


def _normalize_openai_base_url(url: str | None) -> str:
    """Normaliza base_url para que NO termine en /chat/completions."""
    if not url:
        return "https://api.openai.com/v1"
    cleaned = url.strip().rstrip("/")
    if cleaned.endswith("/chat/completions"):
        cleaned = cleaned.rsplit("/chat/completions", 1)[0]
    return cleaned


def _fetch_wso2_token() -> tuple[str, int]:
    """Obtiene un token OAuth2 del gateway WSO2 APIM (client_credentials).
    Mismo patrón que oauth2_apim.py en el directorio AGENT."""
    token_endpoint = os.getenv('WSO2_APIM_TOKEN_ENDPOINT', 'https://localhost:9453/oauth2/token')
    consumer_key    = os.getenv('WSO2_APIM_CONSUMER_KEY', '')
    consumer_secret = os.getenv('WSO2_APIM_CONSUMER_SECRET', '')

    if not consumer_key or not consumer_secret:
        raise RuntimeError("Faltan WSO2_APIM_CONSUMER_KEY / WSO2_APIM_CONSUMER_SECRET en .env")

    creds = f"{consumer_key}:{consumer_secret}"
    basic_auth = base64.b64encode(creds.encode()).decode()

    resp = requests.post(
        token_endpoint,
        headers={
            "Authorization": f"Basic {basic_auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data="grant_type=client_credentials",
        verify=False,
        timeout=15,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Error obteniendo token WSO2: {resp.status_code} - {resp.text}")

    payload = resp.json()
    token = payload.get("access_token")
    if not token:
        raise RuntimeError("No se recibió access_token en la respuesta WSO2")
    expires_in = int(payload.get("expires_in", 3600) or 3600)
    return token, expires_in


class RAGInteractivaDemo:
    def __init__(self):
        load_dotenv()
        
        # 1. Retrieve OpenAI / WSO2 APIM Gateway credentials
        raw_base_url = os.getenv('OPENAI_BASE_URL') or os.getenv('WSO2_OPENAI_API_URL')
        self.openai_base_url = _normalize_openai_base_url(raw_base_url)
        self.embedding_model_name = get_embedding_model_name()
        self.embedding_model = None
        self.http_client = httpx.Client(verify=False, timeout=45.0)
        self.gateway_token = None
        self.gateway_token_expires_at = 0.0

        # 3. Fetch OAuth2 token from WSO2 APIM (same as AGENT/oauth2_apim.py)
        #    and initialize OpenAI client pointing to the gateway
        try:
            token, expires_in = _fetch_wso2_token()
            self.gateway_token = token
            self.gateway_token_expires_at = time.time() + max(60, expires_in - 60)
            print(green("WSO2 OAuth2 token obtained successfully."))
        except Exception as e:
            token = os.getenv('OPENAI_API_KEY', 'unused')
            print(orange(f"\nWARNING: Could not fetch WSO2 token ({e})"))
            print(orange("  Falling back to OPENAI_API_KEY value from .env\n"))

        # 4. Initialize OpenAI client (allow self-signed certs on localhost)
        try:
            client_kwargs: dict = dict(
                api_key=token,
                http_client=self.http_client,
            )
            if self.openai_base_url:
                client_kwargs['base_url'] = self.openai_base_url
            self.openai_client = OpenAI(**client_kwargs)
            print(green("OpenAI client initialized successfully."))
            if self.openai_base_url:
                print(green(f"  Gateway URL: {self.openai_base_url}"))
        except Exception as e:
            self.openai_client = None
            print(orange(f"\nWARNING: Could not initialize OpenAI client: {e}"))
            print(orange("   (The final response generation step will not work)\n"))
            
        self.chunks = []
        self.embeddings = []

    def get_gateway_token(self, force_refresh: bool = False) -> str:
        if not force_refresh and self.gateway_token and time.time() < self.gateway_token_expires_at:
            return self.gateway_token

        token, expires_in = _fetch_wso2_token()
        self.gateway_token = token
        self.gateway_token_expires_at = time.time() + max(60, expires_in - 60)
        return token

    def ensure_embedding_model(self):
        if self.embedding_model is None:
            print(green(f"Loading local embedding model: {self.embedding_model_name}..."))
            print(orange("First use may download the model from Hugging Face and can take several minutes."))
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            print(green("Embedding model loaded successfully."))
    
    def mostrar_banner(self):
        print("\n" + cyan("="*80))
        print(cyan(" " * 20 + "INTERACTIVE RAG DEMO (FREE)"))
        print(cyan("="*80))
        print(blue("Technology: Mistral E5 (Local) + GPT-4o-mini (OpenAI / WSO2 APIM Gateway)"))
        print(blue(f"Embedding model: {self.embedding_model_name}"))
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
        self.ensure_embedding_model()
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
        self.ensure_embedding_model()
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
        print(yellow("STEP 5: GENERATE ANSWER WITH OPENAI (gpt-4o-mini)"))
        print(yellow("-"*80))

        contexto = "\n\n".join([chunk for chunk, _, _ in contextos])

        base_url = _normalize_openai_base_url(self.openai_base_url)
        endpoint = f"{base_url}/chat/completions"

        print(yellow(f"\nSending to OpenAI ({base_url})..."))
        print(blue(f"  - Context length: {len(contexto)} characters"))
        print(blue(f"  - Question: {pregunta}"))
        print(yellow("\nGenerating answer..."))

        try:
            token = self.get_gateway_token()
        except Exception as e:
            token = os.getenv('OPENAI_API_KEY', 'unused')
            print(orange(f"  WARNING: using fallback token ({e})"))

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "Responde siempre en castellano. Usa solo el contexto proporcionado. Sé directo, preciso y breve. Si el contexto no basta, dilo claramente en castellano sin inventar datos."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{contexto}\n\nQuestion: {pregunta}\n\nAnswer:"
                }
            ],
            "temperature": 0.2,
            "max_tokens": 180,
        }

        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            resp = None
            for attempt in range(3):
                resp = self.http_client.post(endpoint, headers=headers, json=payload)
                if resp.status_code in (200, 201):
                    break
                if resp.status_code == 401 and attempt == 0:
                    token = self.get_gateway_token(force_refresh=True)
                    headers["Authorization"] = f"Bearer {token}"
                    continue
                if resp.status_code == 202 and attempt < 2:
                    print(yellow("Gateway devolvió 202 Accepted. Reintentando en breve..."))
                    time.sleep(1.2 * (attempt + 1))
                    continue
                return f"Error calling OpenAI: HTTP {resp.status_code} — {resp.text}"

            if resp is None or resp.status_code not in (200, 201):
                return f"Error calling OpenAI: HTTP {resp.status_code if resp else '000'} — {resp.text if resp else ''}"

            data = resp.json()
            return data["choices"][0]["message"]["content"]

        except Exception as e:
            return f"Error calling OpenAI: {e}"
    
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

from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from pypdf import PdfReader
import ollama
import chromadb
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="documents_v2"
)

DOCUMENTS_DIR = Path("documents")
DOCUMENTS_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {"message": "RAG Document Assistant is running!"}


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def chunk_text(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks


def create_embeddings(chunks):
    embeddings = []

    for chunk in chunks:
        response = ollama.embed(
            model="qwen3-embedding:latest",
            input=chunk
        )

        embeddings.append(response["embeddings"][0])

    return embeddings


def search_documents(query, n_results=3):
    response = ollama.embed(
        model="qwen3-embedding:latest",
        input=query
    )

    query_embedding = response["embeddings"][0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    print("METADATA:", results["metadatas"])

    return results


def generate_rag_answer(query):
    results = search_documents(query)

    relevant_chunks = results["documents"][0]
    sources = results["metadatas"][0]

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are a helpful AI assistant.
Answer the user's question using only the information provided in the context.

Context:
{context}

Question:
{query}

Answer clearly and simply.
"""

    response = ollama.chat(
        model="deepseek-r1:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "answer": response["message"]["content"],
        "sources": sources
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = DOCUMENTS_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_path)

    chunks = chunk_text(text)

    embeddings = create_embeddings(chunks)

    collection.add(
        ids=[f"{file.filename}_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {"source": file.filename}
            for _ in chunks
        ]
    )

    return {
        "message": "PDF processed successfully",
        "filename": file.filename,
        "total_characters": len(text),
        "total_chunks": len(chunks),
        "total_embeddings": len(embeddings)
    }


@app.get("/search")
def search(query: str):
    results = search_documents(query)

    return {
        "query": query,
        "results": results["documents"]
    }


@app.get("/ask")
def ask(query: str):
    answer = generate_rag_answer(query)

    return {
        "question": query,
        "answer": answer["answer"],
        "sources": answer["sources"]
    }
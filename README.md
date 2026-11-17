RAG Document Assistant

Overview

RAG Document Assistant is an AI-powered application that allows users to upload documents and ask questions based on their content. It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information and generate context-aware answers.

Technologies Used

- Python
- FastAPI
- Ollama
- ChromaDB
- DeepSeek LLM

Features

- Upload documents
- Extract text from uploaded documents
- Split documents into smaller chunks
- Generate and store embeddings
- Retrieve relevant information using ChromaDB
- Generate answers using an LLM through Ollama

How It Works

1. The user uploads a document.
2. The application extracts text from the document.
3. The text is divided into smaller chunks.
4. Embeddings are generated and stored in ChromaDB.
5. Relevant chunks are retrieved based on the user's question.
6. The LLM generates an answer using the retrieved context.

Project Structure

rag_document_assistant/
├── frontend/
├── app.py
├── test_chroma.py
├── test_embedding.py
├── test_llm.py
├── requirements.txt
├── README.md
└── .gitignore

Installation

1. Clone the repository:

git clone https://github.com/harini-priya04/RAG-Document-Assistant.git

2. Navigate to the project folder:

cd RAG-Document-Assistant

3. Create a virtual environment:

python -m venv .venv

4. Activate the environment on Windows PowerShell:

.\.venv\Scripts\Activate.ps1

5. Install dependencies:

pip install -r requirements.txt

6. Install and start Ollama separately, then download the model used by the application.

7. Run the application:

uvicorn app:app --reload

LLM Configuration

This project uses DeepSeek-R1:7b through Ollama to generate responses based on retrieved document content.

Model Setup

1. Install Ollama from https://ollama.com/
2. Download the DeepSeek model:

ollama pull deepseek-r1:7b

3. Make sure Ollama is running before starting the application.

The application uses Ollama to run the LLM locally.

Purpose

This project demonstrates the practical implementation of Retrieval-Augmented Generation by combining document retrieval, vector databases and Large Language Models.
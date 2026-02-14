import os
import uuid
from datetime import datetime
from app.config import UPLOAD_DIR
from app.database import insert_document
from app.llm import embed_text
from app.vectorstore import add_chunks

def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def process_document(file, user_id):
    doc_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text)

    embeddings = [embed_text(chunk) for chunk in chunks]
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
    metadatas = [
        {"document_id": doc_id, "document_name": file.filename, "user_id": user_id}
        for _ in chunks
    ]

    add_chunks(ids, embeddings, metadatas, chunks)

    insert_document(doc_id, user_id, file.filename, datetime.utcnow().isoformat())

    return {"doc_id": doc_id, "chunks": len(chunks)}

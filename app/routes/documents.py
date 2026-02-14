from fastapi import APIRouter, Request
from app.database import list_documents, delete_document
import os
from app.config import UPLOAD_DIR
from app.vectorstore import collection

router = APIRouter()

@router.get("/documents")
def get_documents(request: Request):
    user_id = request.session.get("user_id", "default")
    docs = list_documents(user_id)
    return {
        "documents": [
            {"id": doc[0], "name": doc[1], "upload_time": doc[2]}
            for doc in docs
        ]
    }

@router.delete("/documents/{doc_id}")
def remove_document(request: Request, doc_id: str):
    user_id = request.session.get("user_id", "default")
    docs = list_documents(user_id)
    doc = next((d for d in docs if d[0] == doc_id), None)
    if not doc:
        return {"error": "Document not found"}
    
    # Delete from database
    delete_document(doc_id)
    
    # Delete file
    file_path = os.path.join(UPLOAD_DIR, doc[1])
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete from vector store
    try:
        ids = collection.get(where={"document_id": doc_id})["ids"]
        if ids:
            collection.delete(ids=ids)
    except:
        pass
    
    return {"message": "Deleted"}

from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from app.services.document_service import process_document

router = APIRouter()

@router.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files allowed")

    user_id = request.session.get("user_id", "default")
    result = process_document(file, user_id)
    return {"message": "Uploaded successfully", "details": result}

from fastapi import APIRouter
from app.database import get_connection
from app.llm import health_check

router = APIRouter()

@router.get("/status")
def status():
    try:
        conn = get_connection()
        conn.close()
        db_status = "ok"
    except:
        db_status = "error"

    llm_status = "ok" if health_check() else "error"

    return {
        "backend": "ok",
        "database": db_status,
        "llm": llm_status
    }

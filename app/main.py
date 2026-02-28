from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import os
import secrets

from app.database import init_db, verify_user, create_user
from app.routes import upload, ask, status as status_route, documents, chat_history
from app.config import UPLOAD_DIR

app = FastAPI(title="Document RAG Assistant")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize database
init_db()

# Auth middleware
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Public paths
        if request.url.path in ["/login", "/signup", "/static"] or request.url.path.startswith("/static/"):
            return await call_next(request)
        
        # Check authentication
        if not request.session.get("authenticated"):
            # If it's an API call or a non-GET request, return 401
            if request.url.path.startswith("/api/") or request.method in ["POST", "DELETE", "PUT"]:
                return JSONResponse({"detail": "Not authenticated"}, status_code=401)
            # For browser navigation, redirect to login
            return RedirectResponse(url="/login", status_code=302)
        
        return await call_next(request)

# Add middlewares in correct order
app.add_middleware(AuthMiddleware)
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))

# Include API routes with /api prefix
app.include_router(upload.router, prefix="/api")
app.include_router(ask.router, prefix="/api")
app.include_router(status_route.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(chat_history.router, prefix="/api")

# Mount static files (CSS / JS if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates directory
templates = Jinja2Templates(directory="templates")

# Login page
@app.get("/login")
def login_page(request: Request):
    if request.session.get("authenticated"):
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})

# Login handler
@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = verify_user(email, password)
    if user:
        request.session["authenticated"] = True
        request.session["user_id"] = user["id"]
        request.session["user_email"] = user["email"]
        return {"success": True}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Signup handler
@app.post("/signup")
async def signup(request: Request, email: str = Form(...), password: str = Form(...), name: str = Form(None)):
    if create_user(email, password, name):
        # Automatically log in after signup
        request.session["authenticated"] = True
        request.session["user_id"] = email
        request.session["user_email"] = email
        return {"success": True}
    raise HTTPException(status_code=400, detail="User already exists")

# Logout
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    response = RedirectResponse(url="/login", status_code=302)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Home route (UI)
@app.get("/")
def home(request: Request):
    response = templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/documents-page")
def documents_page(request: Request):
    return templates.TemplateResponse(
        "documents.html",
        {"request": request}
    )

@app.get("/status-page")
def status_page(request: Request):
    response = templates.TemplateResponse(
        "status.html",
        {"request": request}
    )
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


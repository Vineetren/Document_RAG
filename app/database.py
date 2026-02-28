from passlib.context import CryptContext
import sqlite3
from app.config import DB_PATH

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            name TEXT,
            upload_time TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            sources TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

def create_user(email, password, full_name=None):
    hashed_password = pwd_context.hash(password)
    user_id = email # Using email as ID for simplicity
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (id, email, hashed_password, full_name) VALUES (?, ?, ?, ?)",
            (user_id, email, hashed_password, full_name)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, hashed_password, full_name FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "email": user[1], "hashed_password": user[2], "full_name": user[3]}
    return None

def verify_user(email, password):
    user = get_user(email)
    if not user:
        return None
    if pwd_context.verify(password, user["hashed_password"]):
        return user
    return None

def insert_document(doc_id, user_id, name, upload_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO documents (id, user_id, name, upload_time) VALUES (?, ?, ?, ?)",
        (doc_id, user_id, name, upload_time)
    )
    conn.commit()
    conn.close()

def list_documents(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, upload_time FROM documents WHERE user_id = ?", (user_id,))
    docs = cursor.fetchall()
    conn.close()
    return docs

def delete_document(doc_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()

def insert_chat_message(user_id, question, answer, sources):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (user_id, question, answer, sources, timestamp) VALUES (?, ?, ?, ?, datetime('now'))",
        (user_id, question, answer, str(sources))
    )
    conn.commit()
    conn.close()

def get_chat_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer, sources, timestamp FROM chat_history WHERE user_id = ? ORDER BY timestamp ASC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"question": r[0], "answer": r[1], "sources": eval(r[2]) if r[2] else [], "timestamp": r[3]} for r in rows]

def clear_chat_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

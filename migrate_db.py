import sqlite3
from app.config import DB_PATH

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if user_id column exists in documents table
    cursor.execute("PRAGMA table_info(documents)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'user_id' not in columns:
        print("Adding user_id column to documents table...")
        cursor.execute("ALTER TABLE documents ADD COLUMN user_id TEXT DEFAULT 'default'")
        conn.commit()
        print("✓ Documents table migrated")
    else:
        print("✓ Documents table already has user_id column")
    
    # Check if chat_history table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_history'")
    if cursor.fetchone():
        # Check if user_id column exists in chat_history table
        cursor.execute("PRAGMA table_info(chat_history)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'user_id' not in columns:
            print("Adding user_id column to chat_history table...")
            cursor.execute("ALTER TABLE chat_history ADD COLUMN user_id TEXT DEFAULT 'default'")
            conn.commit()
            print("✓ Chat history table migrated")
        else:
            print("✓ Chat history table already has user_id column")
    else:
        print("✓ Chat history table doesn't exist yet (will be created on first run)")
    
    conn.close()
    print("\nMigration completed successfully!")

if __name__ == "__main__":
    migrate()

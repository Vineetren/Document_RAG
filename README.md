# Document RAG Assistant

A Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions about them using AI.

## Features Implemented ✅

### Core Functionality
- **Document Upload**: Upload .txt files for processing
- **Question Answering**: Ask questions about uploaded documents
- **Source Citations**: View relevant document excerpts with answers
- **Vector Search**: ChromaDB for semantic document retrieval
- **Smart Chunking**: 800-character chunks with 100-character overlap

### User Experience
- **Authentication**: Session-based login system
- **User Isolation**: Per-user documents and chat history
- **Theme Support**: Light/dark mode with persistence
- **Chat History**: Persistent conversation history per user
- **Real-time Status**: System health monitoring page
- **Responsive UI**: Modern, clean interface with smooth animations

### Advanced Features
- **Intelligent Filtering**: Only shows relevant sources (distance < 1.0)
- **Smart Snippets**: Extracts most relevant 250-char portions
- **Greeting Detection**: Handles casual conversation appropriately
- **Off-topic Redirection**: Politely redirects non-document questions
- **Cross-document Diversity**: Ensures varied source representation

## Setup Instructions

### Prerequisites
- Python 3.8+
- OpenAI API key or OpenRouter API key
- (Optional) [uv](https://github.com/astral-sh/uv) for faster package management

### Installation

1. **Clone the repository**
```bash
cd Doc_Upload_RAG
```

2. **Install dependencies**

Using uv (recommended - faster):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

3. **Configure environment**
Create a `.env` file:
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://openrouter.ai/api/v1
CHAT_MODEL=meta-llama/llama-3.1-8b-instruct
AUTH_USERNAME=admin
AUTH_PASSWORD=demo123
```

4. **Run database migration** (if upgrading from older version)
```bash
python migrate_db.py
```

5. **Start the application**
```bash
uvicorn app.main:app --reload
```

6. **Access the application**
Open browser to: `http://localhost:8000`

Default credentials:
- Username: `admin`
- Password: `demo123`

## Project Structure

```
Doc_Upload_RAG/
├── app/
│   ├── main.py              # FastAPI application & routes
│   ├── config.py            # Configuration & environment variables
│   ├── database.py          # SQLite database operations
│   ├── llm.py              # LLM integration (embeddings & generation)
│   ├── vectorstore.py      # ChromaDB vector store operations
│   ├── routes/             # API route handlers
│   │   ├── upload.py
│   │   ├── ask.py
│   │   ├── documents.py
│   │   ├── status.py
│   │   └── chat_history.py
│   └── services/           # Business logic
│       ├── document_service.py
│       └── qa_service.py
├── templates/              # HTML templates
│   ├── index.html         # Main chat interface
│   ├── login.html         # Login page
│   └── status.html        # System status page
├── static/                # Frontend assets
│   ├── script.js          # JavaScript logic
│   ├── style.css          # Main styles
│   └── auth.css           # Authentication styles
├── data/                  # Data storage (auto-created)
│   ├── uploads/          # Uploaded documents
│   ├── chroma/           # Vector embeddings
│   └── app.db            # SQLite database
├── migrate_db.py         # Database migration script
└── .env                  # Environment configuration
```

## API Endpoints

- `POST /login` - User authentication
- `GET /logout` - User logout
- `POST /upload` - Upload document
- `GET /documents` - List user's documents
- `DELETE /documents/{id}` - Delete document
- `POST /ask` - Ask question
- `GET /chat-history` - Get chat history
- `DELETE /chat-history` - Clear chat history
- `GET /status` - System health check
- `GET /status-page` - Status UI

## Features Not Implemented ❌

- Multi-format support (PDF, DOCX, etc.)
- Document editing/updating
- Advanced search filters
- Export chat history
- Multi-language support
- Voice input/output
- Document sharing between users
- Role-based access control
- API rate limiting
- Batch document upload

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **Vector Store**: ChromaDB
- **LLM**: OpenAI API (via OpenRouter)
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **Icons**: Phosphor Icons
- **Fonts**: Inter (Google Fonts)

## Notes

- Documents are stored per-user and isolated
- Chat history persists across sessions
- Theme preference saved in localStorage
- Vector embeddings use `text-embedding-3-small`
- Chat completions use `meta-llama/llama-3.1-8b-instruct` (configurable via .env)

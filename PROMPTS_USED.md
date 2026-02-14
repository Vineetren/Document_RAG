# Prompts Used During Development

This document records the key prompts used with AI assistants during the development of this RAG application.

## Initial Setup & Architecture

### Project Initialization
```
Create a RAG (Retrieval-Augmented Generation) application using FastAPI that allows users to upload documents and ask questions about them.
```

### Backend Structure
```
Set up a FastAPI backend with routes for document upload, question answering, and document management. Use ChromaDB for vector storage and SQLite for metadata.
```

### Database Design
```
Create a SQLite database schema for storing document metadata with fields for id, name, and upload_time.
```

## Core Features

### Document Upload
```
Implement document upload functionality that:
1. Accepts .txt files
2. Chunks the text into 800-character segments with 100-character overlap
3. Generates embeddings using OpenAI API
4. Stores in ChromaDB with metadata
```

### Question Answering
```
Create a QA service that:
1. Embeds the user's question
2. Retrieves top 6 similar chunks from ChromaDB
3. Ensures cross-document diversity
4. Generates an answer using the LLM with retrieved context
5. Returns answer with source citations
```

### Vector Search Optimization
```
Implement distance-based filtering in the vector search to only return chunks with similarity distance < 1.0
```

## Authentication & Security

### Session-Based Auth
```
Replace HTTP Basic Auth with session-based authentication using FastAPI SessionMiddleware. Create a custom login page with username and password fields.
```

### User Isolation
```
Add user_id to documents and chat_history tables so each user only sees their own data. Filter all queries by user_id from the session.
```

### Logout Functionality
```
Add a logout endpoint that clears the session and redirects to login with cache control headers to prevent back button access.
```

## UI/UX Improvements

### Theme System
```
Implement light/dark mode toggle with:
1. CSS variables for colors
2. localStorage persistence
3. Theme loading before page render to prevent flash
4. Consistent theme across login and main pages
```

### Document Management
```
Add a delete button for each document with:
1. Custom modal confirmation dialog
2. Deletion from database, filesystem, and vector store
3. Auto-refresh of document list
```

### Chat Interface
```
Create a modern chat interface with:
1. User messages on the right with gradient background
2. Bot messages on the left with source citations
3. Smooth animations and scrolling
4. Loading indicator with rotating icon
```

### Source Display
```
Implement smart snippet extraction that:
1. Finds the 250-character portion with most keyword matches
2. Shows relevant excerpts instead of full chunks
3. Removes highlighting for cleaner display
```

## Advanced Features

### Greeting Detection
```
Update the LLM prompt to detect greetings and casual conversation, responding appropriately without showing irrelevant sources.
```

### Off-Topic Redirection
```
Modify the prompt so the assistant politely redirects off-topic questions (sports, personal opinions, etc.) back to document-related queries.
```

### Chat History Persistence
```
Store chat history in the database with user_id, question, answer, sources, and timestamp. Load history on page load to restore previous conversations.
```

### Status Monitoring
```
Create a system status page that checks:
1. Backend API health
2. Database connectivity
3. LLM API connection
Display with color-coded badges and refresh functionality.
```

## Bug Fixes & Refinements

### Double Eye Icon Issue
```
The browser's native password reveal icon appears alongside the custom eye icon in light mode. Add CSS to hide the browser's native icon.
```

### Transparent Modal Issue
```
The delete confirmation modal is transparent and hard to read. Use computed CSS variable values as inline styles to ensure solid background in both themes.
```

### Scrollbar Styling
```
The chat scrollbar is white in dark mode and not positioned correctly. Add custom scrollbar styling that adapts to the theme.
```

### Welcome Message Removal
```
Make the intro message "Hello! Upload a document..." disappear when the user asks their first question.
```

### Source Filtering for Greetings
```
Sources are showing for greetings like "hi" and "good morning". Detect these in the backend and return empty sources array for casual conversation.
```

### Parameter Name Mismatch
```
Fix TypeError where similarity_search() was called with 'k' parameter but the function expects 'top_k'.
```

## Prompt Engineering

### Initial LLM Prompt
```
You are a knowledgeable assistant that answers questions based on provided documents. Answer directly and concisely using ONLY the information from the context.
```

### Improved Prompt with Rules
```
You are a document Q&A assistant. Your ONLY job is to answer questions about the provided documents.

RULES:
1. If user says just "hi", "hello", "hey" etc., respond: "Hi! How can I help you with your documents?"
2. If user asks about anything NOT in the documents, respond: "I'm here to help with questions about your documents..."
3. For questions about the documents, answer using ONLY the context below
4. Do not mention what you cannot find unless the answer is completely absent
5. If asked for a list but only one item exists, provide that item without mentioning the lack of a list
6. Be direct and concise

Mark your response with [CASUAL] or [DOCUMENT] tags.
```

## Database Migration

### Adding User Isolation
```
Create a migration script that adds user_id column to existing documents and chat_history tables without losing data. Set default value to 'default' for existing records.
```

## Documentation

### README Creation
```
Create a comprehensive README with:
1. Setup instructions
2. Features implemented and not implemented
3. Project structure
4. API endpoints
5. Technology stack
```

### AI Notes Documentation
```
Document what AI was used for, what was manually checked, and why specific LLM models were chosen (OpenRouter, GPT-4o-mini, text-embedding-3-small).
```

## Testing Prompts

Throughout development, various testing scenarios were explored:
- "Upload a document and ask questions about it"
- "Test with multiple documents to ensure cross-document retrieval"
- "Verify user isolation by logging in as different users"
- "Test theme persistence across page refreshes"
- "Verify chat history loads correctly after restart"
- "Test greeting detection with various casual phrases"
- "Verify off-topic questions are redirected appropriately"

## Optimization Prompts

### Performance
```
Optimize the vector search to retrieve 6 chunks initially, then filter down to 4 with cross-document diversity.
```

### Code Quality
```
Refactor the source filtering logic to be more maintainable and add comments explaining the keyword matching algorithm.
```

### Security
```
Review the authentication middleware to ensure proper session validation and prevent unauthorized access to API endpoints.
```

---

*Note: These prompts represent the key interactions during development. Many smaller refinements and clarifications occurred throughout the process.*

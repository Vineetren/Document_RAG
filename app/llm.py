import os
from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_BASE_URL, CHAT_MODEL

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

def embed_text(text):
    # Use a cheap embedding model available via OpenRouter
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def generate_answer(context, question):
    prompt = f"""
You are a document Q&A assistant. Your ONLY job is to answer questions about the provided documents.

RULES:
1. If user says just "hi", "hello", "hey" etc., respond: "Hi! How can I help you with your documents?"
2. If user asks about anything NOT in the documents (sports, personal opinions, general knowledge, etc.), respond: "I'm here to help with questions about your documents. Is there anything from the uploaded files you'd like to know?"
3. For questions about the documents, answer using ONLY the context below
4. Do not mention what you cannot find unless the answer is completely absent
5. If document info is completely missing, say: "I don't have that information in the provided documents"
6. If asked for a list but only one item exists, provide that item without mentioning the lack of a list
7. Be direct and concise

Mark your response:
- [CASUAL] for greetings or off-topic questions
- [DOCUMENT] for document-related questions

Context:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content
    
    # Check if LLM marked it as casual conversation
    is_casual = answer.startswith('[CASUAL]')
    if is_casual:
        answer = answer.replace('[CASUAL]', '').strip()
    elif answer.startswith('[DOCUMENT]'):
        answer = answer.replace('[DOCUMENT]', '').strip()
    
    return answer, is_casual

def health_check():
    try:
        _ = embed_text("health check")
        return True
    except Exception as e:
        print("LLM Health Error:", e)
        return False

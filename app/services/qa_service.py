from app.llm import embed_text, generate_answer
from app.vectorstore import similarity_search


def answer_question(question, user_id):
    # Step 1: Embed the question
    query_embedding = embed_text(question)

    # Step 2: Retrieve top-k similar chunks
    results = similarity_search(query_embedding, user_id, top_k=6)

    if not results or not results.get("documents"):
        return {
            "answer": "No relevant documents found.",
            "sources": []
        }

    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Step 3: Ensure cross-document diversity
    selected = []
    seen_docs = set()

    # First pass: pick one chunk per document
    for chunk, meta in zip(chunks, metadatas):
        doc_name = meta.get("document_name", "Unknown Document")

        if doc_name not in seen_docs:
            selected.append((chunk, meta))
            seen_docs.add(doc_name)

        if len(selected) >= 4:
            break

    # Second pass: fill remaining slots if fewer than 4
    if len(selected) < 4:
        for chunk, meta in zip(chunks, metadatas):
            if (chunk, meta) not in selected:
                selected.append((chunk, meta))
            if len(selected) >= 4:
                break

    # Step 4: Prepare context
    selected_chunks = [chunk for chunk, _ in selected]
    selected_metadatas = [meta for _, meta in selected]

    context = "\n\n".join(selected_chunks)

    # Step 5: Generate answer
    answer, is_casual = generate_answer(context, question)

    # Step 6: Prepare sources (empty if casual conversation)
    sources = []
    if not is_casual:
        sources = [
            {
                "document_name": meta.get("document_name", "Unknown Document"),
                "content": chunk
            }
            for chunk, meta in zip(selected_chunks, selected_metadatas)
        ]

    return {
        "answer": answer,
        "sources": sources
    }

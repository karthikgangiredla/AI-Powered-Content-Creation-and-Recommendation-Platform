from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from content_creator import generate_article, save_full_article
from embedder import get_similar_articles
from db_connector import get_connection
import os

app = FastAPI()

# --------------------------- REQUEST MODELS ---------------------------

class GenerateRequest(BaseModel):
    topic: str
    template: str = "templates/developer_advocate.json"
    username: str
    email: str

class SimilarRequest(BaseModel):
    query: str
    top_k: int = 2

# --------------------------- ENDPOINTS ---------------------------

@app.post("/generate")
def generate_article_api(req: GenerateRequest):
    article = generate_article(req.topic, req.template)
    article_id = save_full_article(
        topic=req.topic,
        content=article,
        author=req.username,
        personality=os.path.basename(req.template).replace(".json", ""),
        model_name="gemini",
        email=req.email
    )
    return {"message": "Article created and stored", "title": req.topic, "content": article, "article_id": article_id}


@app.post("/similar")
def get_similar(req: SimilarRequest):
    results = get_similar_articles(req.query, req.top_k)
    return {
        "results": [
            {"id": doc_id, "title": meta["title"]}
            for doc_id, meta in zip(results["ids"][0], results["metadatas"][0])
        ]
    }

@app.get("/articles/{article_id}")
def get_article(article_id: int):
    print(f"🔍 Looking for article ID: {article_id}")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, author, created_at FROM articles WHERE id = %s", (article_id,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Article not found")

    return {
        "id": result[0],
        "title": result[1],
        "content": result[2],
        "author": result[3],
        "created_at": result[4]
    }
@app.get("/debug/articles")
def debug_articles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM articles")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1]} for row in rows]

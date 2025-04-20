from fastapi import FastAPI
from pydantic import BaseModel
from content_creator import generate_article, save_article
from embedder import embed_and_store, get_similar_articles
from db_connector import get_connection

app = FastAPI()

class SimilarRequest(BaseModel):
    query: str
    top_k: int = 5

class GenerateRequest(BaseModel):
    topic: str
    template: str = "templates/developer_advocate.json"
    model: str = "gemini"

@app.post("/generate")
def generate_article_api(req: GenerateRequest):
    article = generate_article(req.topic, req.template)
    save_article(title=req.topic, content=article, author="Developer Advocate")
    embed_and_store(article_id=1, text=article, title=req.topic) 
    return {"message": "Article created and stored", "title": req.topic, "content": article}


@app.post("/similar")
def get_similar(req: SimilarRequest):
    results = get_similar_articles(req.query, req.top_k)
    return {
        "results": [
            {"id": doc_id, "title": meta["title"]}
            for doc_id, meta in zip(results["ids"][0], results["metadatas"][0])
        ]}

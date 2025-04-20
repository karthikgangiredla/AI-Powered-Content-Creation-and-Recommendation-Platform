from fastapi import FastAPI
from pydantic import BaseModel
from content_creator import generate_article, save_full_article
from embedder import get_similar_articles
import os

app = FastAPI()

class GenerateRequest(BaseModel):
    topic: str
    template: str = "templates/developer_advocate.json"
    username: str
    email: str

@app.post("/generate")
def generate_article_api(req: GenerateRequest):
    article = generate_article(req.topic, req.template)
    save_full_article(
    topic=req.topic,
    content=article,
    author=req.username,
    personality=os.path.basename(req.template).replace(".json", ""),
    model_name="gemini",
    email=req.email)

    return {"message": "Article created and stored", "title": req.topic, "content": article}


class SimilarRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/similar")
def get_similar(req: SimilarRequest):
    results = get_similar_articles(req.query, req.top_k)
    return {
        "results": [
            {"id": doc_id, "title": meta["title"]}
            for doc_id, meta in zip(results["ids"][0], results["metadatas"][0])
        ]
    }

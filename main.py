"""from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from content_creator import generate_article, save_full_article
from embedder import get_similar_articles
from db_connector import get_connection
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

class GenerateRequest(BaseModel):
    topic: str
    template: str = "prompts/developer_advocate.json"
    username: str
    email: str

class SimilarRequest(BaseModel):
    query: str
    top_k: int = 2

@app.post("/generate")
def generate_article_api(req: GenerateRequest):
    try:
        print(f" Received request: {req.dict()}")
        article = generate_article(req.topic, req.template)
        print(" Article generated, saving...")

        article_id = save_full_article(
            topic=req.topic,
            content=article,
            author=req.username,
            personality=os.path.basename(req.template).replace(".json", ""),
            model_name="gemini",
            email=req.email
        )
        print(" Article saved with ID:", article_id)

        return {
            "message": "Article created and stored",
            "title": req.topic,
            "content": article,
            "article_id": article_id
        }
    except Exception as e:
        print(" ERROR in /generate:", e)
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


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

@app.get("/articles/{article_id}/html", response_class=HTMLResponse)
def view_article_html(article_id: int, request: Request):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
    article = cursor.fetchone()
    conn.close()

    if not article:
        return HTMLResponse("<h2>Article not found</h2>", status_code=404)

    return templates.TemplateResponse("article.html", {
        "request": request,
        "title": article["title"],
        "content": article["content"],
        "author": article["author"]
    })


"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from content_creator import generate_article, save_full_article
from embedder import get_similar_articles
from db_connector import get_connection
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from logger import logger
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

class GenerateRequest(BaseModel):
    topic: str
    template: str = "prompts/developer_advocate.json"
    username: str
    email: str

class SimilarRequest(BaseModel):
    query: str
    top_k: int = 2

@app.post("/generate")
def generate_article_api(req: GenerateRequest):
    try:
        logger.info(f" Received request: {req.dict()}")
        article = generate_article(req.topic, req.template)
        logger.info(" Article generated, saving...")

        article_id = save_full_article(
            topic=req.topic,
            content=article,
            author=req.username,
            personality=os.path.basename(req.template).replace(".json", ""),
            model_name="gemini",
            email=req.email
        )
        logger.info(f" Article saved with ID: {article_id}")

        return {
            "message": "Article created and stored",
            "title": req.topic,
            "content": article,
            "article_id": article_id
        }
    except Exception as e:
        logger.error(f" ERROR in /generate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.post("/similar")
def get_similar(req: SimilarRequest):
    logger.info(f"🔍 Similarity search for query: {req.query}")
    results = get_similar_articles(req.query, req.top_k)
    logger.info(f" Found {len(results['ids'][0])} similar articles")
    return {
        "results": [
            {"id": doc_id, "title": meta["title"]}
            for doc_id, meta in zip(results["ids"][0], results["metadatas"][0])
        ]
    }

@app.get("/articles/{article_id}")
def get_article(article_id: int):
    logger.info(f"🔍 Looking for article ID: {article_id}")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, author, created_at FROM articles WHERE id = %s", (article_id,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        logger.warning(f" Article ID {article_id} not found")
        raise HTTPException(status_code=404, detail="Article not found")

    logger.info(f" Article ID {article_id} found and returned")
    return {
        "id": result[0],
        "title": result[1],
        "content": result[2],
        "author": result[3],
        "created_at": result[4]
    }

@app.get("/debug/articles")
def debug_articles():
    logger.info("📋 Listing all articles (debug)")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM articles")
    rows = cursor.fetchall()
    conn.close()
    logger.info(f" Retrieved {len(rows)} articles")
    return [{"id": row[0], "title": row[1]} for row in rows]

@app.get("/articles/{article_id}/html", response_class=HTMLResponse)
def view_article_html(article_id: int, request: Request):
    logger.info(f"🖥 Rendering HTML for article ID: {article_id}")
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
    article = cursor.fetchone()
    conn.close()

    if not article:
        logger.warning(f" HTML article ID {article_id} not found")
        return HTMLResponse("<h2>Article not found</h2>", status_code=404)

    logger.info(f" HTML article ID {article_id} rendered")
    return templates.TemplateResponse("article.html", {
        "request": request,
        "title": article["title"],
        "content": article["content"],
        "author": article["author"]
    })

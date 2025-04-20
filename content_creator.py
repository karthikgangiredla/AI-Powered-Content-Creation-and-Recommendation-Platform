import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from embedder import embed_and_store
from db_connector import get_connection

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_article(topic, template_path, model="gemini"):
    template_data = load_template(template_path)
    prompt = template_data["prompt"].replace("{topic}", topic)

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    return response.text

def load_template(path):
    with open(path, "r") as f:
        return json.load(f)


def save_full_article(topic, content, author, personality, model_name, email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (author,))
    user = cursor.fetchone()
    if user:
        uid = user[0]
    else:
        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (author, email))
        uid = cursor.lastrowid


    cursor.execute("""
        INSERT INTO articles (title, content, author)
        VALUES (%s, %s, %s)
    """, (topic, content, author))
    article_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO article_revisions (article_id, version, content)
        VALUES (%s, %s, %s)
    """, (article_id, 1, content))

    cursor.execute("""
        INSERT INTO model_performance (model_name, personality, tokens_used, output_length)
        VALUES (%s, %s, %s, %s)
    """, (model_name, personality, 200, len(content)))

    cursor.execute("""
        INSERT INTO user_interactions (user_id, article_id, action)
        VALUES (%s, %s, %s)
    """, (uid, article_id, "generated"))

    conn.commit()
    conn.close()

    embed_and_store(article_id=article_id, text=content, title=topic)
    return article_id

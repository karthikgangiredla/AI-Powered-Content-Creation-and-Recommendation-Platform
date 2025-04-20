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

def save_article(title, content, author="Developer Advocate"):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO articles (title, content, author) VALUES (%s, %s, %s)"
    cursor.execute(query, (title, content, author))
    conn.commit()
    conn.close()

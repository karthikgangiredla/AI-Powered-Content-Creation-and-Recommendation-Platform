#  AI-Powered Content Creation and Recommendation Platform

This project is an end-to-end AI content platform that empowers users to generate high-quality articles using Large Language Models (LLMs) and receive personalized content recommendations based on semantic similarity.

---

##  Features

###  Content Creation Module
- **Model Switchboard**: Choose between `Falcon` and `Gemini` models
- **Personality Templates**: Developer Advocate, System Architect, Sci-Fi Author, Mystery Writer
- **Prompt Engine**: Uses LangChain to generate custom content
- **Revision Tracking**: Articles are version-controlled

###  Database Architecture
- MySQL-based schema with tables for:
  - Articles + revisions
  - Model performance
  - User interactions and feedback
  - User accounts

###  Recommendation Engine
- Uses `sentence-transformers` + `ChromaDB` for vector similarity search
- Retrieves top-K similar articles
- Uses RAG concepts

###  Reader Experience (Streamlit UI)
- Generate content from topic + personality + model
- View similar articles
- Feedback system: views, likes, dislikes
- Login for user history

---

##  Tech Stack

- **LangChain**
- **MySQL + ChromaDB**
- **Sentence-Transformers**
- **HuggingFace & Gemini (Google AI)** via API
- **FastAPI (Backend)** and **Streamlit (Frontend)**

---

##  Setup Instructions

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Create `.env` File
```
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
GEMINI_API_KEY=your_google_gemini_api_key
```

### 3. Setup MySQL Database
```sql
CREATE DATABASE ai_content_db;
USE ai_content_db;
SOURCE final_full_schema.sql;
```

### 4. Run Backend
```bash
uvicorn main:app --reload
```

### 5. Run Frontend
```bash
streamlit run app.py
```



## Folder Structure

```
├── app.py                      # Streamlit frontend
├── main.py                     # FastAPI backend
├── content_creator.py          # Content creation logic
├── embedder.py                 # Vector embedding and search
├── templates/                  # Prompt templates
├── chroma.sqlite3              # Vector store
├── final_full_schema.sql       # Full MySQL schema
├── requirements.txt            # All dependencies
├── .env                        # API keys + DB config
```

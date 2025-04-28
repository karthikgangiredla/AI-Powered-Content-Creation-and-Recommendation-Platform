# AI-Powered Content Creation & Recommendation Platform

An end-to-end intelligent content platform that leverages Large Language Models (LLMs), semantic embeddings, and vector similarity search to generate, store, and recommend high-quality articles. This system supports versioning, user interactions, and modular personalization.

---

##  Features

###  Content Creation
- Generate articles using `Gemini` LLM
- Choose personality templates like:
  - Developer Advocate
  - System Architect
  - Sci-Fi Author
  - Mystery Writer
- LangChain-based dynamic prompt construction
- Automatic article storage with author info and personality label
- Versioning support for content edits

###  Embedding + Recommendation
- Embeds articles using `sentence-transformers`
- Stores vectors in `ChromaDB` for fast retrieval
- Retrieves top-K similar articles via semantic similarity
- Utilizes RAG (Retrieval-Augmented Generation) concepts for enhancement

###  User Management
- User registration + login via Streamlit
- Secure password storage with hashing
- Tracks individual contributions and preferences

###  Streamlit UI
- **Page 1: Content Creation**
  - Enter topic, choose personality
  - Generate article and view results
- **Page 2: Suggested Articles**
  - Browse saved content
  - View recommendations + interact

###  Debug & Testing Endpoints
- `GET /debug/articles`: List all stored articles
- `GET /articles/{id}/html`: Render article in Markdown
- `POST /similar`: Get similar articles by text input

---

##  Tech Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **LLMs**: Gemini (Google)
- **Embeddings**: Sentence-Transformers
- **Database**: MySQL
- **Vector Store**: ChromaDB
- **Middleware**: LangChain

---

##  Folder Structure
```
.
├── app.py                      # Streamlit app (UI + Auth + Routing)
├── pages/
│   ├── 1_Content_Creation.py   # Streamlit page for article generation
│   └── 2_Suggested_Content.py  # Streamlit page for viewing & suggesting articles
├── main.py                     # FastAPI backend APIs (generation + similarity)
├── content_creator.py          # Article generation logic using LLMs + LangChain
├── embedder.py                 # Vector embedding & similarity search with ChromaDB
├── auth.py                     # User auth (signup/login), password hashing
├── db_connector.py             # Utility for MySQL DB connection
├── prompts/                    # Prompt templates in JSON (personality-based)
│   ├── developer_advocate.json
│   ├── system_architect.json
│   └── sci_fi_author.json
├── final_full_schema.sql       # Complete schema for MySQL (articles, users, etc.)
├── chroma.sqlite3              # Local persistent vector store for embeddings (ChromaDB)
├── frontend/
│   ├── static/
│   │   ├── styles.css          # Optional custom styles (not actively used in Streamlit)
│   │   └── 404.css             # Optional 404 page styling (for Flask or HTML frontend)
│   └── templates/
│       ├── article.html        # HTML template to render full article (used in /articles/{id}/html)
│       └── 404.html            # 404 error page (used by FastAPI fallback)
├── requirements.txt            # List of required Python packages
├── .env                        # Environment variables (API keys, DB credentials)
```

---

##  Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create `.env` File
```env
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
GEMINI_API_KEY=your_google_gemini_api_key
```

### 3. Initialize MySQL DB
```sql
CREATE DATABASE ai_content_db;
USE ai_content_db;
SOURCE final_full_schema.sql;
```

### 4. Launch Backend
```bash
uvicorn main:app --reload
```

### 5. Launch Frontend
```bash
streamlit run app.py
```

### Login Page

![alt text](<images/Screenshot 2025-04-26 112425.png>)


### Content Creation Page
![alt text](<images/Screenshot 2025-04-26 112605.png>)

### Suggest Content page
![alt text](<images/Screenshot 2025-04-26 112652.png>)
![alt text](<images/Screenshot 2025-04-26 112704.png>)
---

##  Versioning & Embeddings
When an article is revised:
- A new entry is created in the revisions table.
- You can re-embed the updated version to update similarity results.
- ChromaDB can store version-tagged vectors or replace old ones depending on strategy.

---

##  Future Enhancements
- User analytics dashboard
- Multilingual content generation
- Fine-tuned models for domain-specific personalization
- Feedback-driven re-ranking
- UI for managing versions and embeddings

---

>  Built using Gemini, LangChain, ChromaDB & Streamlit


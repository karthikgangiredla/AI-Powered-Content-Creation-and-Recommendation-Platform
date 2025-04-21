import streamlit as st
from db_connector import get_connection

if "authenticated" not in st.session_state or not st.session_state.get("authenticated"):
    st.warning(" Please login from the Home page to continue.")
    st.stop()

st.title(" Medium-Style Articles")

conn = get_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT id, title FROM articles ORDER BY id DESC")
articles = cursor.fetchall()
conn.close()

if not articles:
    st.info("No articles found yet.")
    st.stop()

options = [f"{a['id']}: {a['title']}" for a in articles]
selected = st.selectbox("Choose an article to read", options)

if selected:
    try:
        article_id = int(selected.split(":")[0])
    except Exception:
        st.error("Error extracting article ID.")
        st.stop()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT title, content, author FROM articles WHERE id = %s", (article_id,))
    article = cursor.fetchone()
    conn.close()

    if article:
        st.subheader(article["title"])
        st.write(f"Written  by {article['author']}")
        st.markdown(article["content"], unsafe_allow_html=True)
    else:
        st.warning(" Article not found.")

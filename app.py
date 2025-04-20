import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Content Platform", layout="wide")
st.title(" AI-Powered Content Platform")

st.sidebar.header("👤 User Login")
username = st.sidebar.text_input("Username")
email = st.sidebar.text_input("Email (optional)")
user_id = hash(username) % 10000 if username else None
st.sidebar.markdown("---")

st.header(" Generate Article")
topic = st.text_input("Enter a topic")
template = st.selectbox("Choose a personality template", [
    "developer_advocate.json",
    "system_architect.json",
    "sci_fi_author.json",
    "mystery_writer.json"
])
model = "gemini"

if st.button("Generate Article") and topic:
    with st.spinner("Generating..."):
        response = requests.post("http://localhost:8000/generate", json={
            "topic": topic,
            "template": f"templates/{template}"
        })

        
        if response.ok:
            data = response.json()
            st.subheader(data["title"])
            st.write(data["content"])
        else:
            st.error("Failed to generate article.")
            st.write(response.text)


st.header("🔍 Find Similar Articles")
query = st.text_input("Enter a query to search similar articles")
top_k = st.slider("Top K", min_value=1, max_value=10, value=5)

if st.button("Find Similar") and query:
    with st.spinner("Searching..."):
        response = requests.post("http://localhost:8000/similar", json={
            "query": query,
            "top_k": top_k
        })
        if response.ok:
            results = response.json()["results"]
            st.subheader("🔗 Top Matches:")
            for r in results:
                st.markdown(f"**{r['title']}** (ID: {r['id']})")
        else:
            st.error("Similarity search failed.")

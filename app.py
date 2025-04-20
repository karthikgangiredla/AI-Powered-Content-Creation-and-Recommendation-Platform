import streamlit as st
import requests

st.set_page_config(page_title="AI Content Platform", layout="wide")
st.title("AI-Powered Content Platform")
st.sidebar.header(" User Login")
username = st.sidebar.text_input("Username")
email = st.sidebar.text_input("Email (for signup only)")
user_id = hash(username) % 10000 if username else None
st.sidebar.markdown("---")
st.header("Generate Article")
topic = st.text_input("Enter a topic")
template = st.selectbox("Choose a personality template", [
    "developer_advocate.json",
    "system_architect.json",
    "sci_fi_author.json",
    "mystery_writer.json"
])

generated_article = None
generate_btn = st.button("Generate Article", key="generate_btn")

if generate_btn and topic and username:
    response = requests.post("http://localhost:8000/generate", json={
        "topic": topic,
        "template": f"templates/{template}",
        "username": username,
        "email": email
    })

    if response.ok:
        data = response.json()
        generated_article = data["content"]
        st.subheader(data["title"])
        st.write(generated_article)
    else:
        st.error(" Failed to generate article.")
elif generate_btn and not username:
    st.warning(" Please enter a username in the sidebar before generating.")

st.header("🔍 Find Similar Articles")
query = st.text_input("Enter a query to search similar articles")
top_k = st.slider("Top K", min_value=1, max_value=10, value=5)
similarity_btn = st.button("Find Similar", key="similarity_btn")

if similarity_btn and query:
    response = requests.post("http://localhost:8000/similar", json={"query": query, "top_k": top_k})
    if response.ok:
        results = response.json()["results"]
        st.subheader("🔗 Top Matches:")
        for r in results:
            st.markdown(f"**{r['title']}** (ID: {r['id']})")
    else:
        st.error(" Failed to fetch similar articles.")
import streamlit as st
import requests

if "authenticated" not in st.session_state or not st.session_state.get("authenticated"):
    st.warning("🔐 Please login from the Home page to continue.")
    st.stop()

st.set_page_config(page_title="AI Content Creation Platform", layout="wide")
st.title(" AI-Powered Content Platform")

st.sidebar.header("👤 User Info")

st.sidebar.markdown(f"**Username:** {st.session_state.get('username', 'Unknown')}")
st.sidebar.markdown("---")

st.header(" Generate Article")
topic = st.text_input("Enter a topic")


template_display = {
    "Developer Advocate": "developer_advocate",
    "System Architect": "system_architect",
    "Sci-Fi Author": "sci_fi_author",
    "Mystery Writer": "mystery_writer"
}
template_label = st.selectbox("Choose a personality template", list(template_display.keys()))
template = template_display[template_label]
username = st.session_state.get("username", "Unknown")
email = st.session_state.get("email", "Unknown")


generate_btn = st.button("Generate Article", key="generate_btn")

if generate_btn and topic:
    response = requests.post("http://localhost:8000/generate", json={
        "topic": topic,
        "template": f"prompts/{template}.json",
        "username": username,
        "email": email
    })

    if response.ok:
        data = response.json()
        article_id = data["article_id"]
        article_url = f"http://localhost:8000/articles/{article_id}/html"
        generated_article = data["content"]

        st.subheader(data["title"])
        st.write(generated_article)
        st.success(" Article generated successfully!")
        
        sim_response = requests.post("http://localhost:8000/similar", json={
            "query": generated_article,
            "top_k": 3
        })

    else:
        st.error(" Failed to generate article.")
elif generate_btn:
    st.warning(" Please enter a topic before generating.")


import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Content Platform", layout="centered")
st.title("🧠 AI-Powered Content Platform")

# Optional user ID for personalization
st.sidebar.title("👤 User")
user_id = st.sidebar.text_input("User ID (optional)", value="guest")

action = st.radio("What would you like to do?", ["📝 Generate Article", "🔍 Find Similar Articles", "🎯 Smart Recommendations"])

if action == "📝 Generate Article":
    st.header("Generate New Article")
    topic = st.text_input("Enter a topic")

    if st.button("Generate"):
        with st.spinner("Creating your article..."):
            try:
                res = requests.post(f"{API_URL}/generate", json={"topic": topic})
                if res.status_code == 200:
                    data = res.json()
                    st.success("✅ Article Generated!")
                    st.subheader(data["title"])
                    st.divider()
                    st.markdown(data["content"])
                    article_id = data["article_id"]

                    # Track read as feedback
                    if user_id != "guest":
                        requests.post(f"{API_URL}/feedback", json={
                            "article_id": article_id,
                            "feedback": "read",
                            "user_id": user_id
                        })

                    # Feedback buttons
                    if st.button("👍 Like"):
                        requests.post(f"{API_URL}/feedback", json={
                            "article_id": article_id,
                            "feedback": "like",
                            "user_id": user_id
                        })
                        st.success("Thanks for your feedback!")
                    if st.button("👎 Dislike"):
                        requests.post(f"{API_URL}/feedback", json={
                            "article_id": article_id,
                            "feedback": "dislike",
                            "user_id": user_id
                        })
                        st.success("Thanks for your feedback!")

                    # Show similar articles in sidebar
                    st.sidebar.header("🧠 Similar Articles")
                    try:
                        sim = requests.post(f"{API_URL}/similar", json={
                            "query": data["content"], "top_k": 5
                        })
                        if sim.status_code == 200:
                            for result in sim.json()["results"]:
                                st.sidebar.markdown(f"- {result['title']}")
                        else:
                            st.sidebar.warning("Couldn't load similar articles.")
                    except:
                        st.sidebar.warning("⚠️ Could not load similar articles.")
                else:
                    st.error("❌ Error generating article")
            except Exception as e:
                st.error(f"❌ Exception: {e}")

elif action == "🔍 Find Similar Articles":
    st.header("Search Similar Articles")
    query = st.text_input("Search Query")
    top_k = st.slider("How many similar articles?", 1, 10, 5)

    if st.button("Search"):
        with st.spinner("Searching..."):
            try:
                res = requests.post(f"{API_URL}/similar", json={"query": query, "top_k": top_k})
                if res.status_code == 200:
                    st.success("✅ Results found!")
                    results = res.json()["results"]
                    for result in results:
                        st.markdown(f"- **{result['title']}** (ID: `{result['id']}`)")
                else:
                    st.error("❌ Error searching")
            except Exception as e:
                st.error(f"❌ Exception: {e}")

elif action == "🎯 Smart Recommendations":
    st.header("Get Personalized Recommendations")
    query = st.text_input("What are you interested in?")
    top_k = st.slider("Number of results", 1, 10, 5)

    if st.button("Recommend"):
        with st.spinner("Retrieving smart recommendations..."):
            try:
                payload = {"query": query, "top_k": top_k}
                if user_id != "guest":
                    payload["user_id"] = user_id
                res = requests.post(f"{API_URL}/recommend", json=payload)
                if res.status_code == 200:
                    results = res.json()["results"]
                    for result in results:
                        st.markdown(f"- **{result['title']}** (ID: `{result['id']}`) — 🔥 score: `{result['score']}`")
                else:
                    st.error("❌ Failed to get recommendations")
            except Exception as e:
                st.error(f"❌ Exception: {e}")

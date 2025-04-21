import streamlit as st
from auth import create_user_table, register_user, authenticate_user
st.set_page_config(page_title="AI Platform", layout="wide")
create_user_table()


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.title("🔐 Login or Signup")

if not st.session_state.authenticated:
    choice = st.radio("Choose action", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email") if choice == "Signup" else ""

    if st.button("Submit"):
        if choice == "Signup":
            register_user(username, email, password)
            st.success("User registered! You can now login.")
        else:
            if authenticate_user(username, password):
                st.success(" Logged in successfully!")
                st.session_state.authenticated = True
                st.session_state.username = username
            else:
                st.error(" Invalid credentials.")
else:
    st.success("Welcome! Use the sidebar to navigate pages.")
st.success("User registered! Please login below.")



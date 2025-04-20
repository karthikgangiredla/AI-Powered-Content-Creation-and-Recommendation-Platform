from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = ChatGoogleGenerativeAI(
    model="models/gemini-pro",  # or try just "gemini-pro"
    google_api_key=os.getenv("GEMINI_API_KEY")
)

response = llm.invoke("Tell me about vector databases")
print(response)
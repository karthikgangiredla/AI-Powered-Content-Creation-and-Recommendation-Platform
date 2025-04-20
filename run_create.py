from content_creator import generate_article, save_full_article

topic = "general question"
author = "karthik"
template_path = "templates/developer_advocate.json"
model_name = "gemini"
personality = "developer_advocate"

article = generate_article(topic, template_path)

save_full_article(
    topic=topic,
    content=article,
    author=author,
    user_id=1,
    personality=personality,
    model_name=model_name
)

print("Article generated, stored, and tracked across all tables.")

from content_creator import generate_article, save_article

topic = "Vector Databases"
article = generate_article(topic, "templates/developer_advocate.json")

save_article(title=topic, content=article)

print("Article generated and saved to DB.")

from embedder import embed_and_store
embed_and_store(article_id=1, text=article, title=topic)

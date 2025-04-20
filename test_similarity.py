from embedder import get_similar_articles

query = "Explain vector databases and how they work"
results = get_similar_articles(query_text=query)

print("Top Similar Articles:")
for idx, meta in enumerate(results["metadatas"][0]):
    print(f"{idx + 1}. {meta['title']} (ID: {results['ids'][0][idx]})")

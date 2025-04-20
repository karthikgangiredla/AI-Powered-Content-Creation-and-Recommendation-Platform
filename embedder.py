import chromadb
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

chroma_client = chromadb.PersistentClient(path="./chroma_storage")
collection = chroma_client.get_or_create_collection(name="articles")

def embed_and_store(article_id, text, title):
    embedding = embedding_model.encode(text).tolist()

    collection.add(
        documents=[text],
        ids=[str(article_id)],
        metadatas=[{"title": title}]
    )
    print(f"Stored article {article_id} in ChromaDB.")

def get_similar_articles(query_text, top_k=5):
    query_embedding = embedding_model.encode(query_text).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    for idx, metadata in enumerate(results["metadatas"][0]):
        print(f"{idx+1}. {metadata['title']} (ID: {results['ids'][0][idx]})")

    return results

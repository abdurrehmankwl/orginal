from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings()

db = FAISS.load_local("vector_store/", embeddings=embedding, allow_dangerous_deserialization=True)


def get_similar_docs(query, k=4):
    return db.similarity_search(query, k=k)
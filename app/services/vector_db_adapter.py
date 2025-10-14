import os
import chromadb
from app.core.config import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma

class VectorDBAdapter:
    def __init__(self):
        os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
        self.client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)
        self.embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vector_store = Chroma(
            client=self.client,
            collection_name=settings.VECTOR_DB_COLLECTION,
            embedding_function=self.embedding_function,
        )

    def upsert(self, docs, metadatas, ids):
        self.vector_store.add_texts(
            texts=docs,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text, top_k=5, filter=None):
        return self.vector_store.similarity_search(
            query=query_text,
            k=top_k,
            filter=filter
        )

    def as_retriever(self):
        return self.vector_store.as_retriever()
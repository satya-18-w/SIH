import os
from app.core.config import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

class VectorDBAdapter:
    def __init__(self):
        os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
        os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY
        
        self.pinecone = Pinecone(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENVIRONMENT)
        self.embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vector_store = PineconeVectorStore.from_existing_index(
            index_name=settings.PINECONE_INDEX_NAME,
            embedding=self.embedding_function
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

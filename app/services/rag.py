import os
from sqlalchemy.orm import Session
from app.core.config import settings
from app.services.vector_db_adapter import VectorDBAdapter

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

class RagService:
    def __init__(self, db: Session):
        self.db = db
        self.vector_db = VectorDBAdapter()
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro")

    def process_query(self, query: str):
        # 1. Define a retriever
        retriever = self.vector_db.as_retriever()

        # 2. Define a prompt template
        template = """
        You are an expert oceanographer's assistant. Given the following context about ARGO float profiles, answer the user's query.
        If you need to generate a SQL query, it must be a read-only SELECT query on the 'observations' or 'profiles' table.

        Context:
        {context}

        Query: {question}

        Answer:
        """
        prompt = ChatPromptTemplate.from_template(template)

        # 3. Define the RAG chain
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        # 4. Invoke the chain
        response = chain.invoke(query)
        
        # For PoC, we retrieve docs again to show provenance
        retrieved_docs = self.vector_db.query(query_text=query, top_k=5)
        context_docs = [doc.page_content for doc in retrieved_docs]
        provenance_meta = [doc.metadata for doc in retrieved_docs]


        return {
            "query": query,
            "retrieved_context": context_docs,
            "llm_response": response,
            "provenance": provenance_meta
        }

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings
import os


class Model_:

    @staticmethod
    def groqchat_model():
        llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.LLM_MODEL,
            temperature=0.7
        )
        return llm

    embeddings = HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL
    )
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()


class Model_:

    @staticmethod
    def groqchat_model():
        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.3-70b-versatile",
            temperature=0.7
        )
        return llm

    @staticmethod
    def embeddings():
        return HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )
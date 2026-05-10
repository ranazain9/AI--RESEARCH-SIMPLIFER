from langchain_community.vectorstores import FAISS

def vector_(chunk,embedings):
    vector=FAISS.from_documents(chunk,embedings)
    return vector
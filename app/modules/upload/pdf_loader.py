from langchain_community.document_loaders import PyPDFLoader

class Loader_:

    @staticmethod
    def load_pdf(path):
        pdf_loader = PyPDFLoader(path)
        docs = pdf_loader.load()
        return docs
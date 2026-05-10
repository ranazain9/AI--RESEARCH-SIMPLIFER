from langchain_text_splitters import RecursiveCharacterTextSplitter


def Split_Text(doc):
    splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    )

    chunk=splitter.split_documents(doc)
    return chunk
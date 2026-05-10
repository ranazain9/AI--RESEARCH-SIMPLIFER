
def formatDocs(retrieve_docs):
    context_str = "\n\n".join([d.page_content for d in retrieve_docs])
    return context_str
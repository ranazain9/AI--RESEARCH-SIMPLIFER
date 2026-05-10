def retrives(vector):
    retriever1=vector.as_retriever(
        search_type='mmr',
        search_kwargs={"k":6, "lambda_mult":0}
    )
    return retriever1
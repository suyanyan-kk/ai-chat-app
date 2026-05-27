from sentence_transformers import (
    CrossEncoder
)

# =========================
# rerank model
# =========================
rerank_model = CrossEncoder(

    "BAAI/bge-reranker-v2-m3"
)


# =========================
# rerank
# =========================
def rerank_documents(
        query,
        documents,
        top_n=5
):

    """
    documents:

    [
        {
            "content": "...",
            "metadata": {...}
        }
    ]
    """

    if not documents:

        return []

    # =========================
    # build pairs
    # =========================
    sentence_pairs = [

        [query, doc["content"]]

        for doc in documents
    ]

    # =========================
    # predict
    # =========================
    scores = rerank_model.predict(
        sentence_pairs
    )

    # =========================
    # merge
    # =========================
    results = []

    for doc, score in zip(
            documents,
            scores
    ):

        doc["rerank_score"] = float(score)

        results.append(doc)

    # =========================
    # sort
    # =========================
    results.sort(

        key=lambda x: x["rerank_score"],

        reverse=True
    )

    # =========================
    # top n
    # =========================
    return results[:top_n]


from collections import defaultdict

from app.rag.hybrid.bm25_service import (
    bm25_service
)

from app.rag.vectorstore.chroma_service import (
    vector_store
)


class HybridRetrievalService:

    def __init__(self):
        # RRF 参数 k，通常设置在 50-100 之间。这个参数控制了排名位置对最终得分的影响程度。
        # 较小的 k 值会使得排名靠前的文档得分更高，而较大的 k 值则会使得排名位置的影响减弱。
        # 倒数排名融合（Reciprocal Rank Fusion, RRF）是一种简单而有效的融合方法，
        # 它通过对不同检索系统返回的文档进行排名位置的加权来计算最终得分。
        # RRF 的核心思想是：对于每个文档，根据它在不同检索系统中的排名位置，计算一个融合得分。
        # 具体来说，RRF 的得分计算公式如下：
        # RRF_score(d) = ∑ (1 / (k + rank_i(d)))
        # 其中，rank_i(d) 是文档 d 在第 i 个检索系统中的排名位置，k 是一个常数参数。
        # RRF 的优点在于它能够有效地融合多个检索系统的结果，尤其是在不同系统之间存在较大差异时。
        # 通过调整 k 参数，可以控制排名位置对最终得分的影响程度，从而在不同的应用场景中获得更好的性能。
        self.rrf_k = 60

    # =========================
    # vector retrieval
    # =========================
    def vector_search(
            self,
            query,
            top_k=20
    ):

        results = vector_store.similarity_search(

            query=query,

            k=top_k
        )

        formatted_results = []

        for item in results:

            metadata = item.metadata

            formatted_results.append({

                "content":
                    item.page_content,

                "metadata":
                    metadata,

                "source":
                    "vector"
            })

        return formatted_results

    # =========================
    # bm25 retrieval
    # =========================
    def bm25_search(
            self,
            query,
            top_k=20
    ):

        results = bm25_service.search(

            query=query,

            top_k=top_k
        )

        for item in results:

            item["source"] = "bm25"

        return results

    # =========================
    # rrf merge
    # =========================
    def reciprocal_rank_fusion(

            self,

            vector_results,

            bm25_results
    ):

        rrf_scores = defaultdict(float)

        document_map = {}

        # =========================
        # vector rrf
        # =========================
        for rank, doc in enumerate(
                vector_results
        ):

            doc_id = self.build_doc_id(
                doc
            )

            rrf_scores[doc_id] += (

                1 / (self.rrf_k + rank + 1)
            )

            document_map[doc_id] = doc

        # =========================
        # bm25 rrf
        # =========================
        for rank, doc in enumerate(
                bm25_results
        ):

            doc_id = self.build_doc_id(
                doc
            )

            rrf_scores[doc_id] += (

                1 / (self.rrf_k + rank + 1)
            )

            document_map[doc_id] = doc

        # =========================
        # merge
        # =========================
        merged_results = []

        for doc_id, score in rrf_scores.items():

            doc = document_map[doc_id]

            doc["rrf_score"] = score

            merged_results.append(doc)

        # =========================
        # sort
        # =========================
        merged_results.sort(

            key=lambda x: x["rrf_score"],

            reverse=True
        )

        return merged_results

    # =========================
    # build doc id
    # =========================
    def build_doc_id(
            self,
            doc
    ):

        metadata = doc["metadata"]

        return (

            f'{metadata.get("file_id")}_'

            f'{metadata.get("parent_id")}_'

            f'{metadata.get("child_index")}'
        )

    # =========================
    # hybrid search
    # =========================
    def search(
            self,
            query,
            top_k=20
    ):

        # vector
        vector_results = self.vector_search(

            query=query,

            top_k=top_k
        )

        # bm25
        bm25_results = self.bm25_search(

            query=query,

            top_k=top_k
        )

        # merge
        merged_results = \
            self.reciprocal_rank_fusion(

                vector_results,

                bm25_results
            )

        return merged_results


hybrid_retrieval_service = \
    HybridRetrievalService()
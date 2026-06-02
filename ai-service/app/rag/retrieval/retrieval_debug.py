from app.rag.hybrid.hybrid_service import (
    hybrid_retrieval_service 
)
from app.rag.rerank.rerank_service import (
    rerank_documents
)

from app.rag.query.query_analysis_service import (
    analyze_query
)
from app.knowledgedb.db import ( 
    SessionLocal
)
# =========================
# retrieval pipeline debug
# =========================
def retrieval_pipeline_debug(
        query: str,
        recall_k: int = 20,
        rerank_top_k: int = 5
):
    
    # 分析查询
    db = SessionLocal()

    analysis = analyze_query(
        db,
        query
    )

    db.close()
    print("\n========== Debug Query Analysis ==========\n")   
    print(f"Debug Original Query: {analysis.original_query}")
    print(f"Debug Rewritten Query: {analysis.rewritten_query}")
    print(f"Debug Multi Queries: {analysis.multi_queries}")
    print(f"Debug Metadata Filter: {analysis.metadata_filter}") 
    
    all_recall_results = []
    vector_results_by_query = []
    bm25_results_by_query = []
    for q in analysis.multi_queries:
        
        results = (
            hybrid_retrieval_service.search(
                query=q,
                top_k=recall_k,
                metadata_filter=None,
                debug=True
            )
        )
        
        print(f"\nDebug Retrieval Results for Query: {q}\n")
        print(f"Vector Results: {results['vector_results']}")
        print(f"BM25 Results: {results['bm25_results']}") 
        print(f"All Recall Results: {results['all_recall_results']}")  
        bm25_results_by_query.append({ 
            "query": q,
            "bm25_results": results['bm25_results']
        })
        vector_results_by_query.append({ 
            "query": q,
            "vector_results": results['vector_results']
        })  
        all_recall_results.append({

            "query": q,

            "count": len(results["all_recall_results"]),

            "results": results["all_recall_results"]
        })
    merged = []

    seen = set()

    for item in all_recall_results:

        query_text = item["query"]

        for doc in item["results"]:

            doc["recall_query"] = query_text

            parent_id = (
                doc["metadata"]
                .get("parent_id")
            )

            if parent_id in seen:
                continue

            seen.add(parent_id)

            merged.append(doc)

    rerank_results = rerank_documents(
        query=analysis.rewritten_query,
        documents=merged,
        top_n=rerank_top_k
    )


    return {

        "original_query": query,

        "multi_queries": analysis.multi_queries,

        "all_recall_results": all_recall_results,

        "vector_results": vector_results_by_query,

        "bm25_results": bm25_results_by_query,

        "rerank": rerank_results
        }





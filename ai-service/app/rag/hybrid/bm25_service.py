from rank_bm25 import BM25Okapi

from app.knowledgedb.db import SessionLocal

from app.knowledgedb import models

class BM25Service:

    def __init__(self):

        self.documents = []

        self.metadatas = []

        self.bm25 = None

    # =========================
    # load chunks
    # =========================
    def load_documents(self):

        db = SessionLocal()

        chunks = db.query(
            models.KnowledgeChunk
        ).all()

        self.documents = []

        self.metadatas = []

        for chunk in chunks:

            self.documents.append(
                chunk.content
            )

            self.metadatas.append({

                "file_id": chunk.file_id,

                "chunk_id": chunk.id,

                "meta_info": chunk.meta_info,
            })

        db.close()

    # =========================
    # build bm25
    # =========================
    def build_index(self):

        tokenized_docs = [
            # 默认按空格切割字符串。你可以根据需要使用更复杂的分词器。
            # BM25Okapi 不懂句子，只懂单词，所以需要先把文档切分成单词列表。
            doc.split() 

            for doc in self.documents
        ]
        # 创建 BM25 检索器。
        # BM25Okapi 会根据输入的文档列表构建一个索引，以便后续进行检索。
        # BM25 会计算什么？
        # 1. 词出现了几次（TF）
        # 2. 词在多少文档中出现过（DF）
        # 3. 文档长度（DL）
        # 4. 平均文档长度（avgDL）
        # BM25Okapi 会根据这些统计信息来计算 BM25 分数，以衡量查询与文档的相关性。
        self.bm25 = BM25Okapi(
            tokenized_docs
        )

    # =========================
    # init
    # =========================
    def initialize(self):

        self.load_documents()

        self.build_index()

    # =========================
    # search
    # =========================
    def search(
            self,
            query,
            top_k=5
    ):

        if not self.bm25:

            self.initialize()
        # 分词
        tokenized_query = query.split()
        # 打分
        """BM25Okapi 的 get_scores 方法会计算查询与每个文档的相关性分数。
        
        具体来说，get_scores 方法会根据 BM25 算法计算每个文档的分数，分数越高表示文档与查询越相关。
        
        self.documents = [
            "Vue3 生命周期 mounted",
            "Python 基础语法",
            "Vue3 setup 执行顺序"
        ]

        BM25 可能返回：

        scores = [
            8.92,
            0.11,
            7.45
        ]
        """
        scores = self.bm25.get_scores(
            tokenized_query
        )

        results = []

        for idx, score in enumerate(scores):

            results.append({

                "content":
                    self.documents[idx],

                "metadata":
                    self.metadatas[idx],

                "bm25_score":
                    float(score)
            })

        results.sort(

            key=lambda x: x["bm25_score"],

            reverse=True
        )

        return results[:top_k]


bm25_service = BM25Service()
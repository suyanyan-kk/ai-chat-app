import re
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

from app.rag.embedding.embedding_service import (
    embedding_model
)


class SemanticBaseSplitter:

    def __init__(
            self,
            window_size=3,#每次看前后3句 
            percentile=20,#最低20%的 similarity 认为可能是语义断层
            min_chunk_size=150,#避免：chunk 太小
            max_chunk_size=1200#避免：chunk 太大
    ):

        self.window_size = window_size

        self.percentile = percentile

        self.min_chunk_size = min_chunk_size

        self.max_chunk_size = max_chunk_size

    # =========================
    # sentence split
    # 作用把长文本切成句子
    # =========================
    def split_sentences(self, text):

        sentences = re.split(
            r'(?<=[。！？\n])',# 在：。！？换行后面切。
            text
        )

        return [
            s.strip()
            for s in sentences
            if s.strip()
        ]

    # =========================
    # build windows
    # 制造小语义块
    # =========================
    def build_windows(self, sentences):

        windows = []

        for i in range(len(sentences)):

            start = max(
                0,
                i - self.window_size
            )

            end = min(
                len(sentences),
                i + self.window_size
            )

            window_text = "".join(
                sentences[start:end]
            )

            windows.append(window_text)

        return windows

    # =========================
    # embedding similarity
    # 计算相邻 window 的 similarity
    # =========================
    def calculate_similarities(self, embeddings):

        similarities = []

        for i in range(len(embeddings) - 1):
       # 算两个向量夹角similarity 越高说明语义越接近 similarity越低主题变了
            sim = cosine_similarity(
                [embeddings[i]],
                [embeddings[i + 1]]
            )[0][0]

            similarities.append(sim)

        return similarities

    # =========================
    # percentile boundary
        # # 找切分点
    #  例如：所有 similarity：[0.95, 0.92, 0.88, 0.41]
    #  可能：0.5于是：低于0.5认为是语义断层
    # =========================
    def get_breakpoints(self, similarities):

        if not similarities:

            return []

        threshold = np.percentile(
            similarities,
            self.percentile
        )

        breakpoints = []

        for i, sim in enumerate(similarities):

            if sim <= threshold:

                breakpoints.append(i)

        return breakpoints

    # =========================
    # build chunks
    # 真正生成 chunk
    # =========================
    def build_chunks(
            self,
            sentences,
            breakpoints
    ):

        chunks = []

        current_chunk = []#临时存当前 chunk

        current_length = 0

        for i, sentence in enumerate(sentences):

            current_chunk.append(sentence)

            current_length += len(sentence)
             # 到了语义断层
            should_split = (

                i in breakpoints

                and

                current_length >= self.min_chunk_size
            )
         # 没有语义断层。但是 chunk 太大了，强制切分

            force_split = (
                current_length >= self.max_chunk_size
            )

            if should_split or force_split:

                chunks.append(
                    "".join(current_chunk)
                )

                current_chunk = []

                current_length = 0

        if current_chunk:

            chunks.append(
                "".join(current_chunk)
            )

        return chunks

    # =========================
    # public split
    # 对外入口
    # =========================
    def split(self, text):

        sentences = self.split_sentences(text)

        if len(sentences) <= 1:

            return [text]

        windows = self.build_windows(sentences)

        embeddings = embedding_model.embed_documents(
            windows
        )

        similarities = self.calculate_similarities(
            embeddings
        )

        breakpoints = self.get_breakpoints(
            similarities
        )

        chunks = self.build_chunks(
            sentences,
            breakpoints
        )

        return chunks
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language
)

from app.utils.splitters.types import ChunkData
from app.utils.splitters.chunk_builder import build_chunk


LANGUAGE_MAP = {
    "py": Language.PYTHON,
    "js": Language.JS,
    "ts": Language.TS,
    "java": Language.JAVA,
    "vue": Language.HTML,
}


# 普通文本 splitter
default_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
)


def split_code(
    file_id: int,
    original_name: str,
    uuid_name: str,
    content: str
) -> list[ChunkData]:

    ext = uuid_name.split(".")[-1].lower()

    language = LANGUAGE_MAP.get(ext)

    final_chunks = []

    # =========================
    # fallback 普通文本切割
    # =========================

    if not language:

        chunks = default_splitter.split_text(content)

        for index, chunk in enumerate(chunks):

            final_chunks.append(
                build_chunk(
                    file_id=file_id,
                    original_name=original_name,
                    uuid_name=uuid_name,
                    content=chunk,
                    chunk_index=index,
                    splitter="recursive",
                    locator_type="code",
                    locator_value=index,
                    extra={
                        "file_type": uuid_name.split(".")[-1].lower(),
                        "section": "code",

                        "language": "unknown",

                        "chunk_size": 300,

                        "chunk_overlap": 50,
                    }
                )
            )

        return final_chunks

    # =========================
    # language-aware 切割
    # =========================

    language_splitter = RecursiveCharacterTextSplitter.from_language(
        language=language,
        chunk_size=300,
        chunk_overlap=50
    )

    chunks = language_splitter.split_text(content)

    for index, chunk in enumerate(chunks):

        final_chunks.append(
            build_chunk(
                file_id=file_id,
                original_name=original_name,
                uuid_name=uuid_name,
                content=chunk,
                chunk_index=index,
                splitter="language",
                locator_type="code",
                locator_value=index,
                extra={

                    "section": "code",

                    "language": language.name,

                    "chunk_size": 300,

                    "chunk_overlap": 50,
                }
            )
        )

    return final_chunks
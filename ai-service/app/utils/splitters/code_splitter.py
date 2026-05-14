from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language
)
from app.utils.splitters.types import ChunkData

LANGUAGE_MAP = {
    "py": Language.PYTHON,
    "js": Language.JS,
    "ts": Language.TS,
    "java": Language.JAVA,
    "vue": Language.HTML,
}


def split_code(file_id: int, filename: str, content: str) -> list[ChunkData]:

    ext = filename.split(".")[-1].lower()
    language = LANGUAGE_MAP.get(ext)

    # 普通文本切割
    if not language:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
        )

        chunks = splitter.split_text(content)

        return [
            {
                "file_id": file_id,
                "filename": filename,
                "content": chunk,
                "meta_info":{
                    "source": filename,
                    "file_type": ext,
                    "splitter": "recursive",
                    "section": "code",
                    "chunk_index": index,
                }
            }
              for index, chunk in enumerate(chunks)
        ]

    # 代码语言切割
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=language,
        chunk_size=300,
        chunk_overlap=50
    )

    chunks = splitter.split_text(content)

    return [
        {
            "file_id": file_id,
            "filename": filename,
            "content": chunk,
            "meta_info": {
                "source": filename,
                "file_type": ext,
                "language": language.name,
                "splitter": "language",
                "chunk_index": index
            }
        }
        for index, chunk in enumerate(chunks)
    ]
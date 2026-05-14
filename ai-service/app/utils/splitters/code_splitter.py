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


def split_code(content: str, ext: str) -> list[ChunkData]:

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
                "content": chunk,
                "meta_info": {
                    "file_type": ext,
                    "splitter": "recursive"
                }
            }
            for chunk in chunks
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
            "content": chunk,
            "meta_info": {
                "file_type": ext,
                "language": language.name,
                "splitter": "language"
            }
        }
        for chunk in chunks
    ]
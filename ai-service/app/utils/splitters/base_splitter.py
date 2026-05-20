from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.utils.splitters.chunk_builder import build_chunk
from app.utils.splitters.types import ChunkData
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=[
        "\n\n",
        "\n",
        "。",
        "！",
        "？",
        ".",
        " "
    ]
)


def split_text(file_id: int, original_name: str, uuid_name: str, text: str) -> list[ChunkData]:

    chunks = text_splitter.split_text(text)
    final_chunks = []

    for index, chunk in enumerate(chunks):

        final_chunks.append(
            build_chunk(
                file_id=file_id,
                original_name=original_name,
                uuid_name=uuid_name,
                content=chunk,
                chunk_index=index,
                splitter="recursive",
                locator_type="text",
                locator_value=index,
                extra={
                    "file_type": "text",
                    "chunk_size": 300,
                    "chunk_overlap": 50,
                    "section": "text"
                }
            )
        )

    return final_chunks
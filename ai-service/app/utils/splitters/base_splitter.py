from langchain.text_splitter import RecursiveCharacterTextSplitter
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


def split_text(text: str) -> list[ChunkData]:

    chunks = text_splitter.split_text(text)

    return [
        {
            "content": chunk,
            "meta_info": {
                "splitter": "recursive",
                "chunk_size": 300,
                "chunk_overlap": 50,
            }
        }
        for chunk in chunks
    ]
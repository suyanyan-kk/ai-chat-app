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


def split_text(file_id: int, filename: str, text: str) -> list[ChunkData]:

    chunks = text_splitter.split_text(text)

    return [
        {
            "file_id": file_id,
            "filename": filename,
            "content": chunk,
            "meta_info": {
                "source": filename,
                "file_type": filename.split(".")[-1],
                "splitter": "recursive",
                 "section": "text",
                "chunk_size": 300,
                "chunk_overlap": 50,
                "chunk_index": index
            }
        }
       for index, chunk in enumerate(chunks)
    ]
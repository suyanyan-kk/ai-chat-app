from langchain.text_splitter import MarkdownHeaderTextSplitter,RecursiveCharacterTextSplitter
from app.utils.splitters.types import ChunkData

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)
def split_markdown(file_id: int, filename: str, text: str) -> list[ChunkData]:

    md_docs = markdown_splitter.split_text(text)
    final_chunks = []
    print("chunk数量:", len(md_docs))
    for doc_index, doc in enumerate(md_docs):
        print(f"\n===== chunk {doc_index} =====")
        print("meta_info:", doc.metadata)
        print("content:", doc.page_content)
        small_chunks = recursive_splitter.split_text(
            doc.page_content
        )
        print(f"\n===== small_chunks=====")

        for chunk_index, chunk in enumerate(small_chunks):

            print(f"Small chunk {chunk_index}:", chunk)
            final_chunks.append({
                "file_id": file_id,
                "filename": filename,
                "content": chunk,
                "meta_info": {
                    "source": filename,
                    "file_type": "md",
                    "section": (
                        doc.metadata.get("Header 3")
                        or doc.metadata.get("Header 2")
                        or doc.metadata.get("Header 1")
                        or "unknown"
                    ),
                    "doc_index": doc_index,
                    "chunk_index": chunk_index,
                    "headers": doc.metadata,
                    "splitter": "markdown"
                }
            })
    return final_chunks

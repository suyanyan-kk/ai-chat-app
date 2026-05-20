from langchain.text_splitter import MarkdownHeaderTextSplitter,RecursiveCharacterTextSplitter
from app.utils.splitters.chunk_builder import build_chunk
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
def split_markdown(file_id: int,original_name: str, uuid_name: str, text: str) -> list[ChunkData]:

    md_docs = markdown_splitter.split_text(text)
    final_chunks = []
    global_chunk_index = 0
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

            section = (
                doc.metadata.get("Header 3")
                or doc.metadata.get("Header 2")
                or doc.metadata.get("Header 1")
                or "unknown"
            )
            print(f"Small chunk {chunk_index}:", chunk)
            final_chunks.append(
                build_chunk(
                    file_id=file_id,
                    original_name=original_name,
                    uuid_name=uuid_name,
                    content=chunk,
                    chunk_index=global_chunk_index,
                    splitter="markdown",
                    locator_type="section",
                    locator_value=section,
                    extra={
                        "file_type": "md",
                        "char_count": len(chunk),
                        "doc_index": doc_index,
                        "section": section,
                        "h1": doc.metadata.get("Header 1"),
                        "h2": doc.metadata.get("Header 2"),
                        "h3": doc.metadata.get("Header 3"),
                        "chunk_size": 300,
                        "chunk_overlap": 50
                    }
                )
            )
            global_chunk_index += 1
    return final_chunks

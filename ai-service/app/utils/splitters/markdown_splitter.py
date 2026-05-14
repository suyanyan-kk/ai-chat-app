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
def split_markdown(text: str) -> list[ChunkData]:

    md_docs = markdown_splitter.split_text(text)
    final_chunks = []
    print("chunk数量:", len(md_docs))
    for i, doc in enumerate(md_docs):
        print(f"\n===== chunk {i} =====")
        print("meta_info:", doc.metadata)
        print("content:", doc.page_content)
        small_chunks = recursive_splitter.split_text(
            doc.page_content
        )
        print(f"\n===== small_chunks=====")

        for j, chunk in enumerate(small_chunks):

            print(f"Small chunk {j}:", chunk)
            
            final_chunks.append({
                  "content": chunk,
                  "meta_info": {
                    "splitter": "markdown",
                    "headers": doc.metadata
                    }
                 })
    return final_chunks

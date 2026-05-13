from langchain.text_splitter import (
    MarkdownHeaderTextSplitter
)

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)


def split_markdown(text):

    docs = markdown_splitter.split_text(text)

    return [doc.page_content for doc in docs]
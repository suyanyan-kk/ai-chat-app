from langchain.text_splitter import RecursiveCharacterTextSplitter


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
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


def split_text(text: str):

    chunks = text_splitter.split_text(text)

    return chunks
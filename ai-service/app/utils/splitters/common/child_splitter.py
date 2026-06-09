from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

class ChildSplitter:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=300,

            chunk_overlap=50,

            separators=[
                "\n\n",
                "\n",
                "。",
                "！",
                "？",
                "；",
                "，",
                " "
            ]
        )

    def split(self, text):

        return self.splitter.split_text(text)
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

class ParentSplitter:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=1500,

            chunk_overlap=200,

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
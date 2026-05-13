from utils.splitters.base_splitter import split_text

from utils.splitters.markdown_splitter import (
    split_markdown
)


def get_splitter(file_name):

    ext = file_name.split(".")[-1].lower()

    if ext == "md":
        return split_markdown

    return split_text
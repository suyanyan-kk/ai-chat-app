from app.utils.splitters.pdf_splitter import PDFSplitter

from app.utils.splitters.markdown_splitter import MarkdownSplitter

from app.utils.splitters.word_splitter import WordSplitter

from app.utils.splitters.code_splitter import CodeSplitter

from app.utils.splitters.text_splitter import TextSplitter


class SplitterFactory:

    @staticmethod
    def get_splitter(file_type):

        file_type = file_type.lower()

        mapping = {

            # markdown
            "md": MarkdownSplitter(),
            "markdown": MarkdownSplitter(),

            # code
            "py": CodeSplitter(),
            "js": CodeSplitter(),
            "ts": CodeSplitter(),
            "vue": CodeSplitter(),
            "java": CodeSplitter(),

            # word
            "doc": WordSplitter(),
            "docx": WordSplitter(),

            # pdf
            "pdf": PDFSplitter(),

            # text
            "txt": TextSplitter(),
        }

        # 默认 splitter
        return mapping.get(file_type, TextSplitter())

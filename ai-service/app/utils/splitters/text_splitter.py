from app.utils.splitters.base_splitter import BaseSplitter


class TextSplitter(BaseSplitter):

    def split(self, text):

        return text.split("\n\n")
class MarkdownParser:
    
    def parse(self, file_path):

        with open(file_path, "r", encoding="utf-8") as f:

            text = f.read()

        return [
            {
                "text": text
            }
        ]
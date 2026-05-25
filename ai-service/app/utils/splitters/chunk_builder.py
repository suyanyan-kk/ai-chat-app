import uuid

from app.utils.splitters.common.parent_splitter import ParentSplitter

from app.utils.splitters.common.child_splitter import ChildSplitter


class ChunkBuilder:

    def __init__(self, splitter):

        self.splitter = splitter

        self.parent_splitter = ParentSplitter()

        self.child_splitter = ChildSplitter()

    def build(
            self,
            text,
            source_info
    ):

        results = []

        # 1 文件结构切分
        structure_chunks = self.splitter.split(text)

        # 2 parent chunk
        for structure_index, structure_text in enumerate(structure_chunks):

            parent_chunks = \
                self.parent_splitter.split(structure_text)

            for parent_index, parent_text in enumerate(parent_chunks):

                parent_id = str(uuid.uuid4())

                parent_metadata = {

                    "chunk_type": "parent",

                    "parent_id": parent_id,

                    "file_id": source_info["file_id"],

                    "file_name": source_info["file_name"],

                    "file_type": source_info["file_type"],

                    "structure_index": structure_index,

                    "parent_index": parent_index
                }

                parent_doc = {

                    "id": parent_id,

                    "text": parent_text,

                    "metadata": parent_metadata
                }

                results.append(parent_doc)

                # 3 child chunk
                child_chunks = \
                    self.child_splitter.split(parent_text)

                for child_index, child_text in enumerate(child_chunks):

                    child_metadata = {

                        "chunk_type": "child",

                        "parent_id": parent_id,

                        "file_id": source_info["file_id"],

                        "file_name": source_info["file_name"],

                        "file_type": source_info["file_type"],

                        "structure_index": structure_index,

                        "parent_index": parent_index,

                        "child_index": child_index
                    }

                    child_doc = {

                        "id": str(uuid.uuid4()),

                        "text": child_text,

                        "metadata": child_metadata
                    }

                    results.append(child_doc)

        return results



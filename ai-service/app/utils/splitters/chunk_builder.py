
import uuid

from app.utils.splitters.common.semantic_parent_splitter import (
    SemanticParentSplitter
)

from app.utils.splitters.common.semantic_child_splitter import (
    SemanticChildSplitter
)


class ChunkBuilder:

    def __init__(self, splitter):

        # semantic structure
        self.structure_splitter = splitter

        # semantic parent
        self.parent_splitter = \
            SemanticParentSplitter()

        # semantic child
        self.child_splitter = \
            SemanticChildSplitter()

    def build(
            self,
            text,
            source_info
    ):

        results = []

        # =========================
        # 1 structure split
        # =========================
        structure_chunks = \
            self.structure_splitter.split(text)

        # =========================
        # 2 semantic parent
        # =========================
        for structure_index, structure_text in enumerate(structure_chunks):

            parent_chunks = \
                self.parent_splitter.split(
                    structure_text
                )

            for parent_index, parent_text in enumerate(parent_chunks):

                parent_id = str(uuid.uuid4())

                parent_metadata = {

                    "chunk_type": "parent",

                    "parent_id": parent_id,

                    "file_id":
                        source_info["file_id"],

                    "file_name":
                        source_info["file_name"],

                    "file_type":
                        source_info["file_type"],

                    "page":
                        source_info.get("page"),

                    "structure_index":
                        structure_index,

                    "parent_index":
                        parent_index,

                    "semantic_layer":
                        "parent",

                    "splitter":
                        self.parent_splitter.__class__.__name__,
                }

                parent_doc = {

                    "id": parent_id,

                    "text": parent_text,

                    "metadata": parent_metadata
                }

                results.append(parent_doc)

                # =========================
                # 3 semantic child
                # =========================
                child_chunks = \
                    self.child_splitter.split(
                        parent_text
                    )

                for child_index, child_text in enumerate(child_chunks):

                    child_metadata = {

                        "chunk_type": "child",

                        "parent_id": parent_id,

                        "file_id":
                            source_info["file_id"],

                        "file_name":
                            source_info["file_name"],

                        "file_type":
                            source_info["file_type"],

                        "page":
                            source_info.get("page"),

                        "structure_index":
                            structure_index,

                        "parent_index":
                            parent_index,

                        "child_index":
                            child_index,

                        "semantic_layer":
                            "child",

                        "splitter":
                            self.child_splitter.__class__.__name__,
                    }

                    child_doc = {

                        "id": str(uuid.uuid4()),

                        "text": child_text,

                        "metadata": child_metadata
                    }

                    results.append(child_doc)

        return results 





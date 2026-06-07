from pydantic.v1 import BaseModel, Field


class SearchKnowledgeInput(BaseModel):
    # Field校验
    query: str = Field( 
        description="用户要查询的知识库问题"
    )
print(SearchKnowledgeInput)
print(issubclass(SearchKnowledgeInput, BaseModel))
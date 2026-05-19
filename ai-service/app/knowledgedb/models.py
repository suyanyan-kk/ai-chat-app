# models.py
# 定义知识库的 数据模型/数据库结构
# Created by Suyanyan on 2024/6/20.
from sqlalchemy import Column, Integer, String, Text,Boolean,ForeignKey
from app.knowledgedb.db import Base 
class Knowledge(Base):
    __tablename__ = "knowledge_base"
# primary_key=True主键，index=True索引，String字符串，Text长文本，Integer 数字， nullable=True允许为空
# Text 比 String 能存更多内容 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    parent_id = Column(Integer, nullable=True)
    type = Column(String)  # folder / file
    description = Column(Text, nullable=True)
    is_open = Column(Boolean, default=False) # 这个字段用来控制前端树形结构的展开/收起状态，默认值为 False（收起）
    # 关联文件表的字段，存储文件的唯一标识（如文件名或文件路径）
    file_id = Column(Integer, nullable=True)

class KnowledgeFile(Base):
    __tablename__ = "knowledge_file"
    id = Column(Integer, primary_key=True)
    original_name = Column(String)
    uuid_name = Column(String)
    file_url = Column(String)
    file_size = Column(Integer)
    file_type = Column(String)
    content = Column(Text) # 存储文件内容，方便后续查询和使用
    # 默认值为 "pending"（等待向量化）processing 正在向量化 success	已完成 failed	失败
    embedding_status = Column(String,default="pending")


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunk"
    id = Column(Integer,
        primary_key=True,#主键
        index=True #这个表会有很多条记录，建立索引可以提高查询效率
    )
    # 关联文件属于哪个文件
    file_id = Column(
        Integer,
        ForeignKey("knowledge_file.id") #外键这个字段引用另外一张表的id字段，表示这个chunk属于哪个文件
    )
    # chunk 顺序第几个 chunk 以后需要上下文拼接
    chunk_index = Column(Integer,default=0)

    # chunk 内容
    content = Column(Text)

    meta_info = Column(Text, nullable=True)
    # 向量状态
    embedding_status = Column(String,default="pending")

    # 向量ID（以后给向量库用）Chroma 里的 vector uuid。
    vector_id = Column(String,nullable=True)
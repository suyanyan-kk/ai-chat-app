# models.py
# 定义知识库的 数据模型/数据库结构
# Created by Suyanyan on 2024/6/20.
from sqlalchemy import Column, Integer, String, Text,Boolean
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
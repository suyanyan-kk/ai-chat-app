# PostgreSQL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.core.config import settings
# 加载 .env
load_dotenv()
#获取数据库地址 读取环境变量
DATABASE_URL = settings.DATABASE_URL
# SQLALCHEMY_DATABASE_URL = (
#     "postgresql://suyanyan@localhost:5432/ai_project"
# )
# ai_project 是数据库名称，suyanyan 是用户名，localhost 是数据库服务器地址，5432 是 PostgreSQL 的默认端口号
# 如果你的数据库服务器需要密码，可以在 URL 中添加密码，例如：
# SQLALCHEMY_DATABASE_URL = "postgresql://suyanyan:yourpassword@localhost:5432/ai_project"  

# 创建 engine
# echo=True 会在控制台输出 SQLAlchemy 执行的 SQL 语句，方便调试和查看数据库操作的细节
# =========================
# Engine
# =========================
#
# SQLite 和 PostgreSQL 的连接参数不一样。
#
# SQLite 需要：
#   connect_args={"check_same_thread": False}
#
# PostgreSQL 不需要这个参数。
# =========================

if DATABASE_URL.startswith("sqlite"):

    engine = create_engine(
        DATABASE_URL,
        echo=True,
        connect_args={
            "check_same_thread": False
        }
    )

else:

    engine = create_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True
    )

# 创建 SessionLocal 类，绑定到 engine 上，autocommit=False 表示需要手动提交事务，autoflush=False 表示不会自动刷新对象状态到数据库
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
# Base 是一个基类，所有的数据模型类都要继承这个 Base 类，这样 SQLAlchemy 才能知道这些类对应数据库中的表
Base = declarative_base()




# SQLite
# 优点：
# 1. 轻量级：SQLite 是一个小型的数据库引擎，适合嵌入式应用和小型项目。
# 2. 易于使用：SQLite 不需要安装和配置服务器，数据存储在单个文件中，使用非常方便。
# 3. 跨平台：SQLite 可以在各种操作系统上运行，包括 Windows、Linux 和 macOS。
# 4. 免费和开源：SQLite 是一个免费和开源的数据库引擎，社区支持良好。
# 缺点：
# 1. 性能限制：SQLite 在处理大量数据和高并发访问时性能较差，不适合大型应用。
# 2. 功能限制：SQLite 不支持一些高级数据库功能，如存储过程、触发器和复杂查询优化。
# 
# 引入“创建数据库连接”的工具  
# from sqlalchemy import create_engine
# 引入“创建数据库会话”的工具和“声明式基类”工具
# SessionLocal 用于创建数据库会话，declarative_base 定义“数据表的基类”用于定义数据模型 类似你定义一个 TS interface 的基础类
# from sqlalchemy.orm import sessionmaker, declarative_base
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 会生成一个文件：ai.db
# DATABASE_URL = "sqlite:///./ai.db"
# DATABASE_URL = f"sqlite:///{BASE_DIR}/ai.db"
# sqlite 使用 SQLite，/// 固定写法，ai.db 数据库文件存储在当前目录下，文件名为 ai.db

# 创建“数据库引擎”（engine）
# engine = create_engine(
#     DATABASE_URL,
#     # SQLite 特有的参数，允许多线程访问数据库，适合 FastAPI 这种异步框架
#     connect_args={"check_same_thread": False}  # SQLite 必须加
# )
# 创建一个“生成数据库操作实例”的工厂函数，SessionLocal 是一个类，调用 SessionLocal() 就会创建一个新的数据库会话实例
# SessionLocal = sessionmaker(bind=engine)
# 这个 db 就是：真正用来查数据 / 写数据的对象
# db = SessionLocal()
# Base = declarative_base()
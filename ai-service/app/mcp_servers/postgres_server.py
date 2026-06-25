# mcp_servers/postgres_server.py

import os
import re
import json

import psycopg
from psycopg.rows import dict_row

from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP


load_dotenv()


mcp = FastMCP(
    "ai-service-postgres-mcp"
)


def get_database_url() -> str:
    database_url = (
        os.getenv("DATABASE_URL")
        or os.getenv("POSTGRES_URL")
        or os.getenv("SQLALCHEMY_DATABASE_URL")
    )

    if not database_url:

        raise RuntimeError(
            "未找到数据库连接配置，请在 .env 中配置 DATABASE_URL / POSTGRES_URL / SQLALCHEMY_DATABASE_URL"
        )

    return database_url


def get_connection():
    return psycopg.connect(
        get_database_url(),
        row_factory=dict_row,
    )


def is_readonly_sql(
    sql: str,
) -> bool:
    cleaned = sql.strip().strip(";").lower()

    if not cleaned:

        return False

    # 只允许 select / with
    if not (
        cleaned.startswith("select")
        or cleaned.startswith("with")
    ):

        return False

    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "truncate",
        "grant",
        "revoke",
        "copy",
        "call",
        "execute",
        "merge",
    ]

    for keyword in forbidden_keywords:

        pattern = rf"\b{keyword}\b"

        if re.search(
            pattern,
            cleaned,
        ):

            return False

    # 禁止多语句
    if ";" in cleaned:

        return False

    return True


def apply_limit(
    sql: str,
    limit: int,
) -> str:
    cleaned = sql.strip().strip(";")

    if re.search(
        r"\blimit\b",
        cleaned,
        re.IGNORECASE,
    ):

        return cleaned

    return f"{cleaned} LIMIT {limit}"


@mcp.tool()
def pg_list_tables() -> str:
    """
    列出当前 PostgreSQL 数据库中的业务表。
    """

    sql = """
    SELECT
        table_schema,
        table_name
    FROM information_schema.tables
    WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
    ORDER BY table_schema, table_name
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(sql)

            rows = cur.fetchall()

    return json.dumps(
        rows,
        ensure_ascii=False,
        default=str,
    )


@mcp.tool()
def pg_describe_table(
    table_name: str,
) -> str:
    """
    查看指定 PostgreSQL 表结构。
    """

    sql = """
    SELECT
        column_name,
        data_type,
        is_nullable,
        column_default
    FROM information_schema.columns
    WHERE table_name = %s
    ORDER BY ordinal_position
    """

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                sql,
                (
                    table_name,
                ),
            )

            rows = cur.fetchall()

    return json.dumps(
        rows,
        ensure_ascii=False,
        default=str,
    )


@mcp.tool()
def pg_query_readonly(
    sql: str,
    limit: int = 20,
) -> str:
    """
    执行只读 SQL 查询。

    只允许 SELECT / WITH 查询。
    """

    if not is_readonly_sql(
        sql
    ):

        return "拒绝执行：只允许 SELECT / WITH 只读 SQL 查询。"

    if limit <= 0 or limit > 100:

        limit = 20

    final_sql = apply_limit(
        sql,
        limit,
    )

    with get_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                final_sql
            )

            rows = cur.fetchall()

    return json.dumps(
        rows,
        ensure_ascii=False,
        default=str,
    )


@mcp.tool()
def pg_get_knowledge_files(
    limit: int = 20,
) -> str:
    """
    查询知识库文件列表。
    """

    if limit <= 0 or limit > 100:

        limit = 20

    sql = """
    SELECT
        id,
        file_id,
        file_name,
        file_type,
        created_at
    FROM knowledge_file
    ORDER BY id DESC
    LIMIT %s
    """

    try:

        with get_connection() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    sql,
                    (
                        limit,
                    ),
                )

                rows = cur.fetchall()

    except Exception as e:

        return f"查询 knowledge_file 失败: {str(e)}"

    return json.dumps(
        rows,
        ensure_ascii=False,
        default=str,
    )


if __name__ == "__main__":

    mcp.run(
        transport="stdio"
    )
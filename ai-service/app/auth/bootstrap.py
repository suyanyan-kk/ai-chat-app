from app.auth.service import (
    ensure_bootstrap_admin,
    ensure_default_roles_and_permissions,
)
from app.knowledgedb.db import (
    Base,
    SessionLocal,
    engine,
)
from sqlalchemy import inspect, text


KNOWLEDGE_TABLES = (
    "knowledge_base",
    "knowledge_file",
    "knowledge_chunk",
)


def ensure_knowledge_user_columns() -> None:
    """Add ownership columns to databases created before user isolation."""
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    with engine.begin() as connection:
        for table_name in KNOWLEDGE_TABLES:
            if table_name not in existing_tables:
                continue

            columns = {
                column["name"]
                for column in inspector.get_columns(table_name)
            }
            if "user_id" not in columns:
                connection.execute(
                    text(
                        f"ALTER TABLE {table_name} "
                        "ADD COLUMN user_id INTEGER "
                        "REFERENCES auth_user(id)"
                    )
                )

            connection.execute(
                text(
                    "CREATE INDEX IF NOT EXISTS "
                    f"ix_{table_name}_user_id "
                    f"ON {table_name} (user_id)"
                )
            )


def initialize_auth() -> None:
    Base.metadata.create_all(
        bind=engine
    )
    ensure_knowledge_user_columns()

    db = SessionLocal()

    try:
        ensure_default_roles_and_permissions(
            db
        )
        ensure_bootstrap_admin(
            db
        )
    finally:
        db.close()

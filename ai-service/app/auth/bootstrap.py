from app.auth.service import (
    ensure_bootstrap_admin,
    ensure_default_roles_and_permissions,
)
from app.knowledgedb.db import (
    Base,
    SessionLocal,
    engine,
)


def initialize_auth() -> None:
    Base.metadata.create_all(
        bind=engine
    )

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

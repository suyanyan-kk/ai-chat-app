from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.models import AuthUser
from app.auth.service import (
    get_session_by_access_token,
    get_user_permission_codes,
    get_user_role_codes,
)
from app.knowledgedb.db import SessionLocal


bearer_scheme = HTTPBearer(
    auto_error=False
)


def get_auth_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def unauthorized() -> HTTPException:
    return HTTPException(
        status_code=(
            status.HTTP_401_UNAUTHORIZED
        ),
        detail="登录状态已失效",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )


def get_current_user(
    credentials: (
        HTTPAuthorizationCredentials | None
    ) = Depends(bearer_scheme),
    db: Session = Depends(get_auth_db),
) -> AuthUser:
    if credentials is None:
        raise unauthorized()

    session = get_session_by_access_token(
        db,
        credentials.credentials,
    )

    if session is None:
        raise unauthorized()

    return session.user


def require_permissions(
    *required_permissions: str,
) -> Callable:
    def permission_dependency(
        user: AuthUser = Depends(
            get_current_user
        ),
    ) -> AuthUser:
        if user.is_superuser:
            return user

        user_permissions = set(
            get_user_permission_codes(
                user
            )
        )

        if not set(
            required_permissions
        ).issubset(
            user_permissions
        ):
            raise HTTPException(
                status_code=(
                    status.HTTP_403_FORBIDDEN
                ),
                detail="没有执行该操作的权限",
            )

        return user

    return permission_dependency


def require_roles(
    *required_roles: str,
) -> Callable:
    def role_dependency(
        user: AuthUser = Depends(
            get_current_user
        ),
    ) -> AuthUser:
        if user.is_superuser:
            return user

        if not set(
            required_roles
        ).intersection(
            get_user_role_codes(user)
        ):
            raise HTTPException(
                status_code=(
                    status.HTTP_403_FORBIDDEN
                ),
                detail="当前角色不能执行该操作",
            )

        return user

    return role_dependency

import os

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.auth.config import (
    ACCESS_TOKEN_TTL_SECONDS,
    REFRESH_TOKEN_TTL_SECONDS,
)
from app.auth.models import (
    AuthPermission,
    AuthRole,
    AuthSession,
    AuthUser,
)
from app.auth.security import (
    generate_token,
    hash_password,
    hash_token,
    normalize_email,
    verify_password,
)


DEFAULT_PERMISSIONS = [
    (
        "chat.use",
        "使用 AI 对话",
        "chat",
        "use",
    ),
    (
        "knowledge.read",
        "读取知识库",
        "knowledge",
        "read",
    ),
    (
        "knowledge.write",
        "维护知识库",
        "knowledge",
        "write",
    ),
    (
        "knowledge.manage",
        "管理知识库权限",
        "knowledge",
        "manage",
    ),
    (
        "agent.use",
        "使用 Agent",
        "agent",
        "use",
    ),
    (
        "agent.manage",
        "管理 Agent",
        "agent",
        "manage",
    ),
    (
        "mcp.use",
        "使用 MCP 工具",
        "mcp",
        "use",
    ),
    (
        "mcp.manage",
        "管理 MCP 工具",
        "mcp",
        "manage",
    ),
]


DEFAULT_ROLES = {
    "admin": {
        "name": "管理员",
        "description": "拥有系统全部权限",
        "permissions": {
            permission[0]
            for permission in DEFAULT_PERMISSIONS
        },
    },
    "member": {
        "name": "普通成员",
        "description": "可使用 AI、知识库与安全 MCP 工具",
        "permissions": {
            "chat.use",
            "knowledge.read",
            "agent.use",
            "mcp.use",
        },
    },
}


@dataclass
class SessionTokens:
    access_token: str
    refresh_token: str


def utc_now() -> datetime:
    return datetime.now(
        timezone.utc
    )


def ensure_timezone(
    value: datetime,
) -> datetime:
    if value.tzinfo is None:
        return value.replace(
            tzinfo=timezone.utc
        )

    return value


def ensure_default_roles_and_permissions(
    db: Session,
) -> None:
    permissions = {
        permission.code: permission
        for permission in db.query(
            AuthPermission
        ).all()
    }

    for (
        code,
        name,
        resource,
        action,
    ) in DEFAULT_PERMISSIONS:
        if code in permissions:
            continue

        permission = AuthPermission(
            code=code,
            name=name,
            resource=resource,
            action=action,
        )
        db.add(permission)
        permissions[code] = permission

    db.flush()

    roles = {
        role.code: role
        for role in db.query(
            AuthRole
        ).all()
    }

    for code, definition in DEFAULT_ROLES.items():
        role = roles.get(code)

        if role is None:
            role = AuthRole(
                code=code,
                name=definition["name"],
                description=definition[
                    "description"
                ],
                is_system=True,
            )
            db.add(role)
            roles[code] = role

        role.permissions = [
            permissions[permission_code]
            for permission_code in sorted(
                definition["permissions"]
            )
        ]

    db.commit()


def get_role(
    db: Session,
    code: str,
) -> AuthRole:
    role = db.query(
        AuthRole
    ).filter(
        AuthRole.code == code
    ).first()

    if role is None:
        raise ValueError(
            f"角色不存在: {code}"
        )

    return role


def create_user(
    db: Session,
    *,
    email: str,
    password: str,
    display_name: str,
    role_code: str = "member",
    is_superuser: bool = False,
) -> AuthUser:
    normalized_email = normalize_email(
        email
    )
    normalized_name = display_name.strip()

    if len(password) < 8:
        raise ValueError(
            "密码至少需要 8 个字符"
        )

    if not normalized_name:
        raise ValueError(
            "显示名称不能为空"
        )

    existing = db.query(
        AuthUser
    ).filter(
        AuthUser.email == normalized_email
    ).first()

    if existing:
        raise ValueError(
            "该邮箱已存在"
        )

    role = get_role(
        db,
        role_code,
    )

    user = AuthUser(
        email=normalized_email,
        display_name=normalized_name,
        password_hash=hash_password(
            password
        ),
        is_active=True,
        is_superuser=is_superuser,
        roles=[role],
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def ensure_bootstrap_admin(
    db: Session,
) -> None:
    email = os.getenv(
        "AUTH_BOOTSTRAP_ADMIN_EMAIL"
    )
    password = os.getenv(
        "AUTH_BOOTSTRAP_ADMIN_PASSWORD"
    )
    display_name = os.getenv(
        "AUTH_BOOTSTRAP_ADMIN_NAME",
        "System Administrator",
    )

    if not email and not password:
        return

    if not email or not password:
        raise RuntimeError(
            "AUTH_BOOTSTRAP_ADMIN_EMAIL 和 "
            "AUTH_BOOTSTRAP_ADMIN_PASSWORD 必须同时配置"
        )

    normalized_email = normalize_email(
        email
    )
    user = db.query(
        AuthUser
    ).filter(
        AuthUser.email == normalized_email
    ).first()
    admin_role = get_role(
        db,
        "admin",
    )

    if user is None:
        create_user(
            db,
            email=normalized_email,
            password=password,
            display_name=display_name,
            role_code="admin",
            is_superuser=True,
        )
        return

    user.is_active = True
    user.is_superuser = True

    if admin_role not in user.roles:
        user.roles.append(
            admin_role
        )

    db.commit()


def authenticate_credentials(
    db: Session,
    *,
    email: str,
    password: str,
) -> AuthUser | None:
    user = db.query(
        AuthUser
    ).filter(
        AuthUser.email == normalize_email(
            email
        )
    ).first()

    if (
        user is None
        or not user.is_active
        or not verify_password(
            password,
            user.password_hash,
        )
    ):
        return None

    user.last_login_at = utc_now()

    return user


def create_session(
    db: Session,
    *,
    user: AuthUser,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> SessionTokens:
    access_token = generate_token()
    refresh_token = generate_token()
    now = utc_now()

    db.add(
        AuthSession(
            user_id=user.id,
            access_token_hash=hash_token(
                access_token
            ),
            refresh_token_hash=hash_token(
                refresh_token
            ),
            access_expires_at=now
            + timedelta(
                seconds=(
                    ACCESS_TOKEN_TTL_SECONDS
                )
            ),
            refresh_expires_at=now
            + timedelta(
                seconds=(
                    REFRESH_TOKEN_TTL_SECONDS
                )
            ),
            ip_address=ip_address,
            user_agent=(
                user_agent[:512]
                if user_agent
                else None
            ),
        )
    )
    db.commit()

    return SessionTokens(
        access_token=access_token,
        refresh_token=refresh_token,
    )


def get_session_by_access_token(
    db: Session,
    access_token: str,
) -> AuthSession | None:
    session = db.query(
        AuthSession
    ).filter(
        AuthSession.access_token_hash
        == hash_token(access_token)
    ).first()

    if (
        session is None
        or session.revoked_at is not None
        or ensure_timezone(
            session.access_expires_at
        ) <= utc_now()
        or not session.user.is_active
    ):
        return None

    return session


def rotate_refresh_token(
    db: Session,
    *,
    refresh_token: str,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> tuple[
    AuthUser,
    SessionTokens,
] | None:
    session = db.query(
        AuthSession
    ).filter(
        AuthSession.refresh_token_hash
        == hash_token(refresh_token)
    ).first()

    if (
        session is None
        or session.revoked_at is not None
        or ensure_timezone(
            session.refresh_expires_at
        ) <= utc_now()
        or not session.user.is_active
    ):
        return None

    session.revoked_at = utc_now()
    user = session.user
    tokens = create_session(
        db,
        user=user,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return user, tokens


def revoke_refresh_token(
    db: Session,
    refresh_token: str,
) -> None:
    session = db.query(
        AuthSession
    ).filter(
        AuthSession.refresh_token_hash
        == hash_token(refresh_token)
    ).first()

    if (
        session is not None
        and session.revoked_at is None
    ):
        session.revoked_at = utc_now()
        db.commit()


def get_user_role_codes(
    user: AuthUser,
) -> list[str]:
    return sorted(
        {
            role.code
            for role in user.roles
        }
    )


def get_user_permission_codes(
    user: AuthUser,
) -> list[str]:
    permissions = {
        permission.code
        for role in user.roles
        for permission in role.permissions
    }

    return sorted(
        permissions
    )


def serialize_user(
    user: AuthUser,
) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
        "roles": get_user_role_codes(
            user
        ),
        "permissions": (
            get_user_permission_codes(
                user
            )
        ),
    }

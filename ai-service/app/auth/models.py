from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.knowledgedb.db import Base


auth_user_roles = Table(
    "auth_user_role",
    Base.metadata,
    Column(
        "user_id",
        ForeignKey("auth_user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "role_id",
        ForeignKey("auth_role.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


auth_role_permissions = Table(
    "auth_role_permission",
    Base.metadata,
    Column(
        "role_id",
        ForeignKey("auth_role.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        ForeignKey("auth_permission.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class AuthUser(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True)
    email = Column(String(320), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    token_version = Column(Integer, nullable=False, default=1)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    roles = relationship(
        "AuthRole",
        secondary=auth_user_roles,
        back_populates="users",
        lazy="selectin",
    )
    sessions = relationship(
        "AuthSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class AuthRole(Base):
    __tablename__ = "auth_role"

    id = Column(Integer, primary_key=True)
    code = Column(String(80), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    users = relationship(
        "AuthUser",
        secondary=auth_user_roles,
        back_populates="roles",
    )
    permissions = relationship(
        "AuthPermission",
        secondary=auth_role_permissions,
        back_populates="roles",
        lazy="selectin",
    )


class AuthPermission(Base):
    __tablename__ = "auth_permission"

    id = Column(Integer, primary_key=True)
    code = Column(String(120), unique=True, nullable=False, index=True)
    name = Column(String(120), nullable=False)
    resource = Column(String(80), nullable=False)
    action = Column(String(40), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    roles = relationship(
        "AuthRole",
        secondary=auth_role_permissions,
        back_populates="permissions",
    )


class AuthSession(Base):
    __tablename__ = "auth_session"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("auth_user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    access_token_hash = Column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
    )
    refresh_token_hash = Column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
    )
    access_expires_at = Column(DateTime(timezone=True), nullable=False)
    refresh_expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True, index=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    ip_address = Column(String(64), nullable=True)
    user_agent = Column(String(512), nullable=True)

    user = relationship(
        "AuthUser",
        back_populates="sessions",
        lazy="joined",
    )

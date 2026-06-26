import hashlib
import secrets

import bcrypt


PASSWORD_ROUNDS = 12
TOKEN_BYTES = 48


def normalize_email(
    email: str,
) -> str:
    return email.lower().strip()


def hash_password(
    password: str,
) -> str:
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise ValueError(
            "密码长度不能超过 72 个 UTF-8 字节"
        )

    return bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(
            rounds=PASSWORD_ROUNDS
        ),
    ).decode("utf-8")


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False


def generate_token() -> str:
    return secrets.token_urlsafe(
        TOKEN_BYTES
    )


def hash_token(
    token: str,
) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

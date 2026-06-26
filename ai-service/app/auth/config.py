import os


def env_bool(
    name: str,
    default: bool = False,
) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.lower().strip() in {
        "1",
        "true",
        "yes",
        "on",
    }


ACCESS_TOKEN_TTL_SECONDS = int(
    os.getenv(
        "AUTH_ACCESS_TOKEN_TTL_SECONDS",
        "900",
    )
)

REFRESH_TOKEN_TTL_SECONDS = int(
    os.getenv(
        "AUTH_REFRESH_TOKEN_TTL_SECONDS",
        "604800",
    )
)

REFRESH_COOKIE_NAME = os.getenv(
    "AUTH_REFRESH_COOKIE_NAME",
    "ai_refresh_token",
)

REFRESH_COOKIE_SECURE = env_bool(
    "AUTH_COOKIE_SECURE",
    default=False,
)

REFRESH_COOKIE_SAMESITE = os.getenv(
    "AUTH_COOKIE_SAMESITE",
    "lax",
)

LOGIN_MAX_ATTEMPTS = int(
    os.getenv(
        "AUTH_LOGIN_MAX_ATTEMPTS",
        "5",
    )
)

LOGIN_WINDOW_SECONDS = int(
    os.getenv(
        "AUTH_LOGIN_WINDOW_SECONDS",
        "300",
    )
)

TRUST_PROXY_HEADERS = env_bool(
    "AUTH_TRUST_PROXY_HEADERS",
    default=False,
)

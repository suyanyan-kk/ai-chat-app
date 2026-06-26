from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.auth.config import (
    ACCESS_TOKEN_TTL_SECONDS,
    LOGIN_WINDOW_SECONDS,
    REFRESH_COOKIE_NAME,
    REFRESH_COOKIE_SAMESITE,
    REFRESH_COOKIE_SECURE,
    REFRESH_TOKEN_TTL_SECONDS,
    TRUST_PROXY_HEADERS,
)
from app.auth.dependencies import (
    get_auth_db,
    get_current_user,
)
from app.auth.models import AuthUser
from app.auth.rate_limit import (
    login_rate_limiter,
)
from app.auth.schemas import (
    AuthResponse,
    LoginRequest,
    MessageResponse,
    UserResponse,
)
from app.auth.service import (
    authenticate_credentials,
    create_session,
    revoke_refresh_token,
    rotate_refresh_token,
    serialize_user,
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
) 


def get_client_ip(
    request: Request,
) -> str | None:
    if TRUST_PROXY_HEADERS:
        forwarded_for = request.headers.get(
            "x-forwarded-for"
        )

        if forwarded_for:
            return forwarded_for.split(
                ",",
                1,
            )[0].strip()

    if request.client:
        return request.client.host

    return None


def get_user_agent(
    request: Request,
) -> str | None:
    return request.headers.get(
        "user-agent"
    )


def login_key(
    request: Request,
    email: str,
) -> str:
    return (
        f"{get_client_ip(request) or 'unknown'}"
        f":{email.lower().strip()}"
    )


def set_refresh_cookie(
    response: Response,
    refresh_token: str,
) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        max_age=REFRESH_TOKEN_TTL_SECONDS,
        httponly=True,
        secure=REFRESH_COOKIE_SECURE,
        samesite=REFRESH_COOKIE_SAMESITE,
        path="/",
    )


def clear_refresh_cookie(
    response: Response,
) -> None:
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path="/",
        secure=REFRESH_COOKIE_SECURE,
        httponly=True,
        samesite=REFRESH_COOKIE_SAMESITE,
    )


def build_auth_response(
    access_token: str,
    user: AuthUser,
) -> AuthResponse:
    return AuthResponse(
        access_token=access_token,
        expires_in=ACCESS_TOKEN_TTL_SECONDS,
        user=UserResponse(
            **serialize_user(user)
        ),
    )


def disable_auth_response_cache(
    response: Response,
) -> None:
    response.headers[
        "Cache-Control"
    ] = "no-store"
    response.headers["Pragma"] = "no-cache"


@router.post(
    "/login",
    response_model=AuthResponse,
)
def login(
    data: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_auth_db),
):
    disable_auth_response_cache(
        response
    )
    key = login_key(
        request,
        data.email,
    )

    if login_rate_limiter.is_blocked(
        key
    ):
        raise HTTPException(
            status_code=(
                status.HTTP_429_TOO_MANY_REQUESTS
            ),
            detail="登录尝试过多，请稍后再试",
            headers={
                "Retry-After": str(
                    LOGIN_WINDOW_SECONDS
                )
            },
        )

    user = authenticate_credentials(
        db,
        email=data.email,
        password=data.password,
    )

    if user is None:
        login_rate_limiter.record_failure(
            key
        )
        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail="邮箱或密码错误",
        )

    login_rate_limiter.clear(
        key
    )
    tokens = create_session(
        db,
        user=user,
        ip_address=get_client_ip(
            request
        ),
        user_agent=get_user_agent(
            request
        ),
    )
    set_refresh_cookie(
        response,
        tokens.refresh_token,
    )

    return build_auth_response(
        tokens.access_token,
        user,
    )


@router.post(
    "/refresh",
    response_model=AuthResponse,
)
def refresh(
    request: Request,
    response: Response,
    refresh_token: str | None = Cookie(
        default=None,
        alias=REFRESH_COOKIE_NAME,
    ),
    db: Session = Depends(get_auth_db),
):
    disable_auth_response_cache(
        response
    )
    if not refresh_token:
        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail="缺少刷新凭证",
        )

    result = rotate_refresh_token(
        db,
        refresh_token=refresh_token,
        ip_address=get_client_ip(
            request
        ),
        user_agent=get_user_agent(
            request
        ),
    )

    if result is None:
        clear_refresh_cookie(
            response
        )
        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail="刷新凭证已失效",
        )

    user, tokens = result
    set_refresh_cookie(
        response,
        tokens.refresh_token,
    )

    return build_auth_response(
        tokens.access_token,
        user,
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
)
def logout(
    response: Response,
    refresh_token: str | None = Cookie(
        default=None,
        alias=REFRESH_COOKIE_NAME,
    ),
    db: Session = Depends(get_auth_db),
):
    disable_auth_response_cache(
        response
    )
    if refresh_token:
        revoke_refresh_token(
            db,
            refresh_token,
        )

    clear_refresh_cookie(
        response
    )

    return MessageResponse(
        message="已退出登录"
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    response: Response,
    user: AuthUser = Depends(
        get_current_user
    ),
):
    disable_auth_response_cache(
        response
    )
    return UserResponse(
        **serialize_user(user)
    )

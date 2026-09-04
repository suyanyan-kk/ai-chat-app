import threading

from collections import defaultdict, deque
from time import monotonic

from app.auth.config import (
    LOGIN_MAX_ATTEMPTS,
    LOGIN_WINDOW_SECONDS,
    REGISTER_MAX_ATTEMPTS,
    REGISTER_WINDOW_SECONDS,
)


class LoginRateLimiter:
    def __init__(
        self,
        max_attempts: int = LOGIN_MAX_ATTEMPTS,
        window_seconds: int = LOGIN_WINDOW_SECONDS,
    ):
        self._max_attempts = max_attempts
        self._window_seconds = window_seconds
        self._attempts = defaultdict(
            deque
        )
        self._lock = threading.Lock()

    def _remove_expired(
        self,
        key: str,
        now: float,
    ) -> None:
        attempts = self._attempts[key]
        threshold = (
            now - self._window_seconds
        )

        while (
            attempts
            and attempts[0] <= threshold
        ):
            attempts.popleft()

        if not attempts:
            self._attempts.pop(
                key,
                None,
            )

    def is_blocked(
        self,
        key: str,
    ) -> bool:
        now = monotonic()

        with self._lock:
            self._remove_expired(
                key,
                now,
            )

            return len(
                self._attempts.get(
                    key,
                    ()
                )
            ) >= self._max_attempts

    def record_failure(
        self,
        key: str,
    ) -> None:
        now = monotonic()

        with self._lock:
            self._remove_expired(
                key,
                now,
            )
            self._attempts[key].append(
                now
            )

    def clear(
        self,
        key: str,
    ) -> None:
        with self._lock:
            self._attempts.pop(
                key,
                None,
            )


login_rate_limiter = LoginRateLimiter()
registration_rate_limiter = LoginRateLimiter(
    max_attempts=REGISTER_MAX_ATTEMPTS,
    window_seconds=REGISTER_WINDOW_SECONDS,
)

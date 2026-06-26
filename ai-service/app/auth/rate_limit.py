import threading

from collections import defaultdict, deque
from time import monotonic

from app.auth.config import (
    LOGIN_MAX_ATTEMPTS,
    LOGIN_WINDOW_SECONDS,
)


class LoginRateLimiter:
    def __init__(self):
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
            now - LOGIN_WINDOW_SECONDS
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
            ) >= LOGIN_MAX_ATTEMPTS

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

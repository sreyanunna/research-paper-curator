import time


class RateLimiter:
    """Enforces a minimum gap between actions.

    arXiv asks callers to leave at least 3 seconds between requests.
    We remember when we last acted and, on the next call, sleep only
    for the time still owed.
    """

    def __init__(self, min_interval: float = 3.0):
        self.min_interval = min_interval
        self._last_call = 0.0  # monotonic timestamp of the previous request

    def wait(self) -> None:
        elapsed = time.monotonic() - self._last_call
        remaining = self.min_interval - elapsed

        if remaining > 0:
            print(f"[rate-limit] {elapsed:.2f}s since last call -> sleeping {remaining:.2f}s")
            time.sleep(remaining)
        else:
            print(f"[rate-limit] {elapsed:.2f}s since last call -> no wait")

        self._last_call = time.monotonic()
import time
import logging

import httpx
import feedparser

logger = logging.getLogger(__name__)


class RateLimiter:
    """Enforces a minimum gap between actions (arXiv asks for >= 3s)."""

    def __init__(self, min_interval: float = 3.0):
        self.min_interval = min_interval
        self._last_call = 0.0

    def wait(self) -> None:
        elapsed = time.monotonic() - self._last_call
        remaining = self.min_interval - elapsed
        if remaining > 0:
            time.sleep(remaining)
        self._last_call = time.monotonic()


class ArxivClient:
    """Rate-limited, retry-aware client for the arXiv API."""

    def __init__(
        self,
        base_url: str = "http://export.arxiv.org/api/query",
        rate_limit_delay: float = 3.0,
        max_results: int = 10,
        search_category: str = "cs.AI",
        max_retries: int = 3,
        timeout: float = 30.0,
    ):
        self.base_url = base_url
        self.rate_limit_delay = rate_limit_delay
        self.max_results = max_results
        self.search_category = search_category
        self.max_retries = max_retries
        self.timeout = timeout
        self._limiter = RateLimiter(min_interval=rate_limit_delay)  # the hand-off

    def fetch_papers(self, category: str | None = None, max_results: int | None = None):
        category = category or self.search_category
        max_results = max_results or self.max_results

        params = {
            "search_query": f"cat:{category}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            self._limiter.wait()  # respect the 3s gap before EVERY attempt
            try:
                #response = httpx.get(self.base_url, params=params, timeout=self.timeout)
                response = httpx.get(self.base_url, params=params, timeout=self.timeout, follow_redirects=True)
                response.raise_for_status()
                feed = feedparser.parse(response.text)
                return [
                    {
                        "arxiv_id": entry.id.split("/abs/")[-1],
                        "title": entry.title.strip(),
                        "authors": [a.name for a in entry.authors],
                        "summary": entry.summary.strip(),
                        "published": entry.published,
                    }
                    for entry in feed.entries
                ]
            except httpx.HTTPError as exc:
                last_error = exc
                backoff = self.rate_limit_delay * (2 ** (attempt - 1))
                logger.warning("attempt %d failed: %s -> backing off %.1fs", attempt, exc, backoff)
                time.sleep(backoff)

        raise RuntimeError(f"arXiv fetch failed after {self.max_retries} attempts") from last_error
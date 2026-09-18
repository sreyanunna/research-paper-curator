from src.services.arxiv.client import ArxivClient


def make_arxiv_client() -> ArxivClient:
    """Single place that decides how a client is built."""
    return ArxivClient(
    base_url="https://export.arxiv.org/api/query",   # http -> https
    rate_limit_delay=3.0,
    max_results=10,
    search_category="cs.AI",
)

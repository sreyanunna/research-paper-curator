import logging

from opensearchpy import OpenSearch, helpers

from src.services.opensearch.index_config import ARXIV_PAPERS_INDEX, ARXIV_PAPERS_MAPPING

logger = logging.getLogger(__name__)


class OpenSearchClient:
    """The only place that talks to OpenSearch. Both pipelines use it."""

    def __init__(self, host: str = "http://localhost:9200", index_name: str = ARXIV_PAPERS_INDEX, mapping: dict = ARXIV_PAPERS_MAPPING):
        self.client = OpenSearch(hosts=[host], timeout=30)
        self.index_name = index_name
        self.mapping = mapping

    def health_check(self) -> bool:
        return self.client.ping()

    def create_index(self, recreate: bool = False) -> bool:
        """Create the index from its mapping. Returns True if it was created."""
        exists = self.client.indices.exists(index=self.index_name)
        if exists and not recreate:
            logger.info("index %s already exists, skipping", self.index_name)
            return False
        if exists:
            self.client.indices.delete(index=self.index_name)
        self.client.indices.create(index=self.index_name, body=self.mapping)
        logger.info("created index %s", self.index_name)
        return True

    def index_paper(self, paper: dict) -> None:
        # _id = arxiv_id, so re-indexing the same paper overwrites instead of duplicating
        self.client.index(index=self.index_name, id=paper["arxiv_id"], body=paper)

    def bulk_index_papers(self, papers: list[dict]) -> dict:
        """Index many papers in one request; one bad paper doesn't fail the batch."""
        actions = [{"_index": self.index_name, "_id": p["arxiv_id"], "_source": p} for p in papers]
        success, errors = helpers.bulk(self.client, actions, raise_on_error=False, refresh=True)
        for err in errors:
            logger.warning("failed to index: %s", err)
        return {"indexed": success, "failed": len(errors)}

    def count(self) -> int:
        return self.client.count(index=self.index_name)["count"]
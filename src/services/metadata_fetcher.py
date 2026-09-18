import logging
from pathlib import Path

import httpx

from src.services.arxiv.factory import make_arxiv_client
from src.pdf_parser.docling import DoclingPDFParser

logger = logging.getLogger(__name__)


def run_ingestion(max_results: int = 3, pdf_dir: str = "data/pdfs") -> dict:
    """Lessons 1 + 2, tied together: fetch metadata, download, parse."""
    arxiv_client = make_arxiv_client()
    parser = DoclingPDFParser()          # loads Docling models once, up front
    pdf_dir = Path(pdf_dir)
    pdf_dir.mkdir(parents=True, exist_ok=True)

    papers = arxiv_client.fetch_papers(max_results=max_results)
    logger.info("fetched %d papers from arXiv", len(papers))

    results = {"parsed": [], "failed": []}
    for paper in papers:
        arxiv_id = paper["arxiv_id"]
        try:                                              # <-- error isolation
            pdf_path = _download_pdf(arxiv_id, pdf_dir)
            parsed = parser.parse(pdf_path)
            results["parsed"].append({
                "arxiv_id": arxiv_id,
                "title": paper["title"],
                "markdown_chars": len(parsed["markdown"]),
            })
            logger.info("parsed %s (%d chars)", arxiv_id, len(parsed["markdown"]))
        except Exception as exc:
            logger.warning("FAILED on %s: %s", arxiv_id, exc)
            results["failed"].append({"arxiv_id": arxiv_id, "error": str(exc)})

    logger.info("done: %d parsed, %d failed", len(results["parsed"]), len(results["failed"]))
    return results


def _download_pdf(arxiv_id: str, pdf_dir: Path) -> Path:
    dest = pdf_dir / f"{arxiv_id}.pdf"
    if dest.exists():                                     # <-- caching / idempotency
        logger.info("cache hit, skipping download for %s", arxiv_id)
        return dest

    url = f"https://arxiv.org/pdf/{arxiv_id}"
    logger.info("downloading %s", url)
    resp = httpx.get(url, timeout=60.0, follow_redirects=True)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    return dest

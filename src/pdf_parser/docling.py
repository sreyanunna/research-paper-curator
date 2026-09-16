import logging
from pathlib import Path

from docling.document_converter import DocumentConverter

logger = logging.getLogger(__name__)


class DoclingPDFParser:
    """Turns a scientific PDF into structured, machine-readable content."""

    def __init__(self):
        # Building the converter loads Docling's ML models (layout, tables)
        # into memory. That's why construction is expensive and why we do it
        # ONCE here, not on every parse.
        self._converter = DocumentConverter()

    def parse(self, pdf_path: str | Path) -> dict:
        pdf_path = Path(pdf_path)
        logger.info("parsing %s with Docling", pdf_path.name)

        result = self._converter.convert(str(pdf_path))
        doc = result.document

        return {
            "source": pdf_path.name,
            "markdown": doc.export_to_markdown(),
        }
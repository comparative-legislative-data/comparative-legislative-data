"""
Provenance & Audit Trail Utility Engine
"""

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict
from pydantic import BaseModel, Field, HttpUrl


class Provenance(BaseModel):
    """
    Academic data provenance block enforcing auditability and source traceability.
    """
    source_url: str = Field(..., description="Exact URL of the host legislature API or feed endpoint")
    retrieved_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when data was fetched"
    )
    raw_payload_hash: str = Field(..., description="SHA-256 hash of the raw unmodified source payload")
    scraper_version: str = Field(..., description="Version of the scraper module used")
    license: str = Field(..., description="Open data license governing the host source feed")


def compute_sha256(content: bytes | str) -> str:
    """Computes SHA-256 hex digest for raw payload content."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    return f"sha256:{hashlib.sha256(content).hexdigest()}"


def generate_provenance(
    source_url: str,
    raw_content: bytes | str,
    scraper_version: str,
    license_name: str
) -> Provenance:
    """Helper factory for generating a standardized Provenance model."""
    return Provenance(
        source_url=source_url,
        retrieved_at=datetime.now(timezone.utc),
        raw_payload_hash=compute_sha256(raw_content),
        scraper_version=scraper_version,
        license=license_name
    )

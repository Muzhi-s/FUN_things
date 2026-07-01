"""End-to-end file analysis pipeline for the Streamlit UI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from app.cache import DEFAULT_CACHE_PATH, load_cached_analysis, store_cached_analysis
from app.analyzer import analyze_with_ollama
from app.extractor import extract_pe_metadata
from app.rules import assess_file_risk
from app.scanner import filter_program_files, scan_directory


def scan_program_directory(root_dir: str | Path) -> list[dict[str, Any]]:
    """Scan a directory and return only program-related files."""

    return filter_program_files(scan_directory(root_dir))


def analyze_file(file_path: str | Path, db_path: str | Path = DEFAULT_CACHE_PATH) -> dict[str, Any]:
    """Run metadata extraction, risk assessment, and Ollama analysis with cache."""

    cached_result = load_cached_analysis(file_path, db_path=db_path)
    if cached_result is not None:
        return {**cached_result, "cache_hit": True}

    metadata = extract_pe_metadata(file_path)
    risk_result = assess_file_risk(file_path, metadata)
    model_result = analyze_with_ollama(metadata, risk_result)

    result = {
        "path": str(Path(file_path)),
        "metadata": metadata,
        "risk": risk_result,
        "analysis": model_result,
    }
    store_cached_analysis(file_path, result, db_path=db_path)

    return {**result, "cache_hit": False}

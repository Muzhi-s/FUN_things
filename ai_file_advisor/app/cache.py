"""SQLite cache for file analysis results."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


DEFAULT_CACHE_PATH = Path(__file__).resolve().parents[1] / "database" / "advisor.db"


def load_cached_analysis(file_path: str | Path, db_path: str | Path = DEFAULT_CACHE_PATH) -> dict[str, Any] | None:
    """Return cached analysis when path, size, and modification time still match."""

    target_path = Path(file_path)
    if not target_path.exists():
        return None

    file_signature = _build_file_signature(target_path)
    connection = _connect(db_path)
    try:
        _ensure_schema(connection)
        row = connection.execute(
            """
            SELECT payload_json
            FROM file_analysis_cache
            WHERE file_path = ? AND size = ? AND mtime_ns = ?
            """,
            (file_signature["file_path"], file_signature["size"], file_signature["mtime_ns"]),
        ).fetchone()
        if row is None:
            return None

        return json.loads(row["payload_json"])
    finally:
        connection.close()


def store_cached_analysis(
    file_path: str | Path,
    payload: dict[str, Any],
    db_path: str | Path = DEFAULT_CACHE_PATH,
) -> None:
    """Persist an analysis result for later reuse."""

    target_path = Path(file_path)
    file_signature = _build_file_signature(target_path)
    connection = _connect(db_path)
    try:
        _ensure_schema(connection)
        connection.execute(
            """
            INSERT INTO file_analysis_cache (file_path, size, mtime_ns, payload_json, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(file_path) DO UPDATE SET
                size = excluded.size,
                mtime_ns = excluded.mtime_ns,
                payload_json = excluded.payload_json,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                file_signature["file_path"],
                file_signature["size"],
                file_signature["mtime_ns"],
                json.dumps(payload, ensure_ascii=False, default=str),
            ),
        )
        connection.commit()
    finally:
        connection.close()


def _connect(db_path: str | Path) -> sqlite3.Connection:
    database_path = Path(db_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def _ensure_schema(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS file_analysis_cache (
            file_path TEXT PRIMARY KEY,
            size INTEGER NOT NULL,
            mtime_ns INTEGER NOT NULL,
            payload_json TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )


def _build_file_signature(file_path: Path) -> dict[str, Any]:
    stat_result = file_path.stat()
    return {
        "file_path": str(file_path.resolve()),
        "size": stat_result.st_size,
        "mtime_ns": stat_result.st_mtime_ns,
    }

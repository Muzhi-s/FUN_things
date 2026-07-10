"""使用 SQLite 数据库缓存文件分析结果"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


DEFAULT_CACHE_PATH = Path(__file__).resolve().parents[1] / "database" / "advisor.db"


def load_cached_analysis(file_path: str | Path, db_path: str | Path = DEFAULT_CACHE_PATH) -> dict[str, Any] | None:
    """从缓存中加载指定文件的分析结果"""

    # 文件存在性检查
    target_path = Path(file_path)
    if not target_path.exists():
        return None

    # 构建文件签名并查询缓存
    file_signature = _build_file_signature(target_path)
    
    # 连接数据库
    connection = _connect(db_path)
    try:
        _ensure_schema(connection)
        # 查询缓存(精准匹配)
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
    """将文件分析结果存储到缓存中"""

    target_path = Path(file_path)
    #构建文件签名
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


# 数据库连接和模式管理
def _connect(db_path: str | Path) -> sqlite3.Connection:
    database_path = Path(db_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection

# 保证数据库模式存在
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

# 文件签名构建
def _build_file_signature(file_path: Path) -> dict[str, Any]:
    stat_result = file_path.stat()
    return {
        "file_path": str(file_path.resolve()),
        "size": stat_result.st_size,
        "mtime_ns": stat_result.st_mtime_ns,
    }

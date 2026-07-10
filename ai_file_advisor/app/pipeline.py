"""面向 Streamlit UI 的端到端文件分析流水线。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from app.cache import DEFAULT_CACHE_PATH, load_cached_analysis, store_cached_analysis
from app.analyzer import analyze_with_ollama
from app.extractor import extract_pe_metadata
from app.rules import assess_file_risk
from app.scanner import filter_program_files, scan_directory


def scan_program_directory(root_dir: str | Path) -> list[dict[str, Any]]:
    """扫描指定目录下的所有文件，并返回经过规则过滤后的文件列表。"""

    return filter_program_files(scan_directory(root_dir))


def analyze_file(file_path: str | Path, db_path: str | Path = DEFAULT_CACHE_PATH) -> dict[str, Any]:
    """ 分析指定文件，返回结构化结果，包括元数据、风险评估和 Ollama 分析结果。"""
    
    # 检查缓存
    cached_result = load_cached_analysis(file_path, db_path=db_path)
    if cached_result is not None:
        return {**cached_result, "cache_hit": True}
    # 提取PE元数据
    metadata = extract_pe_metadata(file_path)
    # 评估文件风险
    risk_result = assess_file_risk(file_path, metadata)
    # AI分析
    model_result = analyze_with_ollama(metadata, risk_result)

    # 组合最终结果
    result = {
        "path": str(Path(file_path)),
        "metadata": metadata,
        "risk": risk_result,
        "analysis": model_result,
    }
    # 存储到缓存
    store_cached_analysis(file_path, result, db_path=db_path)

    return {**result, "cache_hit": False}

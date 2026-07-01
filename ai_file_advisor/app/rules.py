"""Basic path-based risk rules for AI File Advisor."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Any


@dataclass(frozen=True)
class RiskResult:
    risk_level: str
    reason: str
    matched_rule: str | None = None


def assess_file_risk(file_path: str | Path, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    """Assess deletion risk using only the file path for now."""

    metadata = metadata or {}
    windows_path = PureWindowsPath(str(file_path))
    path_parts = [part.casefold() for part in windows_path.parts]

    result = _match_path_rules(path_parts)
    return {
        "path": str(file_path),
        "name": windows_path.name,
        "risk_level": result.risk_level,
        "reason": result.reason,
        "matched_rule": result.matched_rule,
        "metadata": metadata,
    }


def _match_path_rules(path_parts: list[str]) -> RiskResult:
    if _contains_parts(path_parts, ["windows"]):
        return RiskResult(
            risk_level="high",
            reason="文件位于 Windows 系统目录，删除可能影响系统稳定性。",
            matched_rule="windows_system_directory",
        )

    if _contains_any_part(path_parts, {"program files", "program files (x86)", "programdata"}):
        return RiskResult(
            risk_level="medium-high",
            reason="文件位于程序安装目录，通常属于已安装软件组件。",
            matched_rule="program_files_directory",
        )

    if _contains_any_part(path_parts, {"downloads"}):
        return RiskResult(
            risk_level="low",
            reason="文件位于下载目录，通常是用户手动下载内容。",
            matched_rule="downloads_directory",
        )

    if _contains_any_part(path_parts, {"temp", "tmp", "temporary internet files"}):
        return RiskResult(
            risk_level="low",
            reason="文件位于临时目录，通常可优先清理，但仍需确认是否正在使用。",
            matched_rule="temporary_directory",
        )

    return RiskResult(
        risk_level="unknown",
        reason="当前规则未覆盖该路径，需要结合文件元信息进一步判断。",
        matched_rule=None,
    )


def _contains_parts(path_parts: list[str], parts: list[str]) -> bool:
    return all(part in path_parts for part in parts)


def _contains_any_part(path_parts: list[str], candidates: set[str]) -> bool:
    return any(part in candidates for part in path_parts)

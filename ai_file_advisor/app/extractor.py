"""PE metadata extraction for executable and DLL files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pefile


def extract_pe_metadata(file_path: str | Path) -> dict[str, Any]:
    """Extract common version metadata from a PE file.

    Returns a dictionary with stable keys even when the file cannot be parsed.
    """

    target_path = Path(file_path)
    metadata: dict[str, Any] = {
        "path": str(target_path),
        "name": target_path.name,
        "is_pe": False,
        "product_name": None,
        "company_name": None,
        "file_description": None,
        "version": None,
        "file_version": None,
        "product_version": None,
    }

    try:
        pe = pefile.PE(str(target_path))
    except (FileNotFoundError, OSError, pefile.PEFormatError):
        return metadata

    try:
        metadata["is_pe"] = True

        string_values = _extract_string_file_info(pe)
        metadata["product_name"] = string_values.get("product_name")
        metadata["company_name"] = string_values.get("company_name")
        metadata["file_description"] = string_values.get("file_description")
        metadata["file_version"] = string_values.get("file_version")
        metadata["product_version"] = string_values.get("product_version")
        metadata["version"] = (
            metadata["file_version"]
            or metadata["product_version"]
            or _extract_fixed_file_version(pe)
        )
        return metadata
    finally:
        close_method = getattr(pe, "close", None)
        if callable(close_method):
            close_method()


def _extract_string_file_info(pe: pefile.PE) -> dict[str, str | None]:
    values: dict[str, str | None] = {
        "product_name": None,
        "company_name": None,
        "file_description": None,
        "file_version": None,
        "product_version": None,
    }

    for file_info_list in getattr(pe, "FileInfo", []) or []:
        for file_info in file_info_list or []:
            if getattr(file_info, "Key", None) != b"StringFileInfo":
                continue

            for string_table in getattr(file_info, "StringTable", []) or []:
                entries = getattr(string_table, "entries", {}) or {}
                for raw_key, raw_value in entries.items():
                    key = _normalize_key(raw_key)
                    value = _normalize_value(raw_value)
                    if key == "productname":
                        values["product_name"] = value
                    elif key == "companyname":
                        values["company_name"] = value
                    elif key == "filedescription":
                        values["file_description"] = value
                    elif key == "fileversion":
                        values["file_version"] = value
                    elif key == "productversion":
                        values["product_version"] = value

    return values


def _extract_fixed_file_version(pe: pefile.PE) -> str | None:
    fixed_infos = getattr(pe, "VS_FIXEDFILEINFO", None) or []
    if not fixed_infos:
        return None

    fixed_info = fixed_infos[0]
    file_version_ms = getattr(fixed_info, "FileVersionMS", None)
    file_version_ls = getattr(fixed_info, "FileVersionLS", None)
    if file_version_ms is None or file_version_ls is None:
        return None

    major = (file_version_ms >> 16) & 0xFFFF
    minor = file_version_ms & 0xFFFF
    build = (file_version_ls >> 16) & 0xFFFF
    revision = file_version_ls & 0xFFFF
    return f"{major}.{minor}.{build}.{revision}"


def _normalize_key(value: Any) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore").strip().casefold()
    return str(value).strip().casefold()


def _normalize_value(value: Any) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore").strip("\x00").strip()
    return str(value).strip()

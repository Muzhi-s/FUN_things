"""针对可执行文件和DLL文件的PE元数据提取。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pefile


def extract_pe_metadata(file_path: str | Path) -> dict[str, Any]:
    """从PE文件中提取通用的版本元数据。返回一个包含key的字典"""
    
    #步骤1: 初始化元数据字典，设置默认值
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

    #步骤2: 尝试加载PE文件，如果失败则返回默认元数据
    try:
        pe = pefile.PE(str(target_path))
    except (FileNotFoundError, OSError, pefile.PEFormatError):
        return metadata

    #步骤3: 提取元数据
    try:
        metadata["is_pe"] = True

        #调用内部函数提取字符串资源
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
        #步骤4：确保PE对象被正确关闭以释放资源
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
        # 查找FileInfo结构
        for file_info in file_info_list or []:
            # 只处理stringFileInfo结构，提取其中的字符串表
            if getattr(file_info, "Key", None) != b"StringFileInfo":
                continue
            
            #遍历string table中的条目，提取所需的元数据
            for string_table in getattr(file_info, "StringTable", []) or []:
                entries = getattr(string_table, "entries", {}) or {}
                #遍历所有键值对
                for raw_key, raw_value in entries.items():
                    key = _normalize_key(raw_key) #标准化键名
                    value = _normalize_value(raw_value) #标准化值

                    #匹配已知的键名
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
    """从PE文件的VS_FIXEDFILEINFO结构中提取文件版本号"""
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

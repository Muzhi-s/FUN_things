from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.pipeline import analyze_file, scan_program_directory


DEFAULT_SCAN_PATH = r"D:\fun_th1ngs\auto_shutdown"


def main() -> None:
    st.set_page_config(page_title="AI File Advisor", page_icon="🗂️", layout="wide")
    _apply_styles()

    st.title("AI File Advisor")
    st.caption("本地文件分析工具 - 当前版本聚焦扫描、提取和基础解释")

    with st.sidebar:
        st.subheader("扫描设置")
        root_dir = st.text_input("目录路径", value=DEFAULT_SCAN_PATH)
        scan_button = st.button("扫描目录", type="primary", use_container_width=True)

    if scan_button:
        try:
            scanned_files = scan_program_directory(root_dir)
            st.session_state["scanned_files"] = scanned_files
            st.session_state["selected_file"] = scanned_files[0]["path"] if scanned_files else None
            st.session_state["analysis_result"] = None
            st.session_state["analysis_file_path"] = None
            st.success(f"扫描完成，共找到 {len(scanned_files)} 个程序类文件。")
        except Exception as exc:
            st.session_state["scanned_files"] = []
            st.session_state["selected_file"] = None
            st.session_state["analysis_result"] = None
            st.session_state["analysis_file_path"] = None
            st.error(f"扫描失败：{exc}")

    scanned_files = st.session_state.get("scanned_files", [])

    if not scanned_files:
        st.info("先在左侧输入目录并点击“扫描目录”。")
        return

    left_column, right_column = st.columns([1.1, 1.4], gap="large")

    with left_column:
        st.subheader("文件列表")
        selected_path = st.selectbox(
            "选择一个文件进行分析",
            options=[item["path"] for item in scanned_files],
            format_func=lambda value: Path(value).name,
            index=_selected_index(scanned_files, st.session_state.get("selected_file")),
        )
        st.session_state["selected_file"] = selected_path

        st.dataframe(
            scanned_files,
            use_container_width=True,
            hide_index=True,
            column_config={
                "path": st.column_config.TextColumn("path", width="large"),
                "name": st.column_config.TextColumn("name"),
                "size": st.column_config.NumberColumn("size", format="%d"),
            },
        )

    with right_column:
        st.subheader("分析结果")
        analyze_button = st.button("分析当前文件", type="primary", use_container_width=True)

        if analyze_button:
            try:
                with st.spinner("正在提取元信息、评估风险并调用 Ollama..."):
                    result = analyze_file(selected_path)
                st.session_state["analysis_result"] = result
                st.session_state["analysis_file_path"] = selected_path
            except Exception as exc:
                st.session_state["analysis_result"] = None
                st.session_state["analysis_file_path"] = None
                st.error(f"分析失败：{exc}")

        analysis_result = st.session_state.get("analysis_result")
        analysis_file_path = st.session_state.get("analysis_file_path")
        if analysis_result and analysis_file_path == selected_path:
            _render_analysis(selected_path, analysis_result)
        else:
            st.info("点击“分析当前文件”后显示元信息、风险结果和模型输出。")


def _render_analysis(selected_path: str, result: dict[str, object]) -> None:
    metadata = result.get("metadata", {})
    risk = result.get("risk", {})
    analysis = result.get("analysis", {})
    cache_hit = result.get("cache_hit", False)

    st.markdown("### 基本信息")
    info_columns = st.columns(3)
    info_columns[0].metric("文件名", metadata.get("name", ""))
    info_columns[1].metric("风险等级", risk.get("risk_level", "unknown"))
    info_columns[2].metric("分析模型", analysis.get("model", ""))

    if cache_hit:
        st.success("已命中缓存，本次未重复执行提取与模型分析。")

    st.markdown("### 元信息")
    st.json(
        {
            "path": metadata.get("path", selected_path),
            "product_name": metadata.get("product_name"),
            "company_name": metadata.get("company_name"),
            "file_description": metadata.get("file_description"),
            "version": metadata.get("version"),
        }
    )

    st.markdown("### 规则结果")
    st.json(
        {
            "risk_level": risk.get("risk_level"),
            "reason": risk.get("reason"),
            "matched_rule": risk.get("matched_rule"),
        }
    )

    st.markdown("### Ollama 输出")
    raw_content = analysis.get("content", "")
    parsed = _try_parse_json(raw_content)
    if parsed is not None:
        st.json(parsed)
    else:
        st.code(str(raw_content), language="text")


def _selected_index(scanned_files: list[dict[str, object]], selected_file: str | None) -> int:
    if not selected_file:
        return 0

    for index, item in enumerate(scanned_files):
        if item.get("path") == selected_file:
            return index
    return 0


def _try_parse_json(content: object) -> dict[str, object] | None:
    if not isinstance(content, str):
        return None

    text = content.strip()
    if not text:
        return None

    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return None

    return value if isinstance(value, dict) else None


def _apply_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #f5f5f5;
            color: #1f1f1f;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e5e5e5;
            border-radius: 12px;
            padding: 0.75rem 1rem;
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid #e5e5e5;
            border-radius: 12px;
            overflow: hidden;
            background: #ffffff;
        }
        .stButton > button {
            background: #222222;
            color: white;
            border-radius: 8px;
            border: none;
        }
        .stButton > button:hover {
            background: #444444;
            color: white;
            border: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

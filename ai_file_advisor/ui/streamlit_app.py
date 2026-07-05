from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.pipeline import analyze_file, scan_program_directory
from ui.answer_view import render_answer_result
from ui.styles import apply_app_styles


DEFAULT_SCAN_PATH = r"D:\fun_th1ngs\auto_shutdown"


def main() -> None:
    st.set_page_config(page_title="AI File Advisor", page_icon="🗂️", layout="wide")
    apply_app_styles()

    with st.sidebar:
        st.title("AI File Advisor")
        st.caption("本地文件分析助手")
        st.divider()
        st.subheader("扫描位置")
        root_dir = st.text_input("目录路径", value=DEFAULT_SCAN_PATH)
        scan_button = st.button("扫描文件", type="primary", use_container_width=True)

    if scan_button:
        try:
            scanned_files = scan_program_directory(root_dir)
            st.session_state["scanned_files"] = scanned_files
            st.session_state["selected_file"] = scanned_files[0]["path"] if scanned_files else None
            st.session_state["analysis_result"] = None
            st.session_state["analysis_file_path"] = None
            st.toast(f"扫描完成，找到 {len(scanned_files)} 个可分析文件。")
        except Exception as exc:
            st.session_state["scanned_files"] = []
            st.session_state["selected_file"] = None
            st.session_state["analysis_result"] = None
            st.session_state["analysis_file_path"] = None
            st.error(f"扫描失败：{exc}")

    scanned_files = st.session_state.get("scanned_files", [])

    if not scanned_files:
        _render_empty_state()
        return

    selected_path = _render_file_picker(scanned_files)

    st.markdown("### 分析结果")
    analyze_button = st.button("分析当前文件", type="primary", use_container_width=True)

    if analyze_button:
        try:
            with st.spinner("正在生成文件建议..."):
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
        render_answer_result(selected_path, analysis_result)
    else:
        st.info("选择文件后点击分析，页面会直接给出用途、风险和处理建议。")


def _render_empty_state() -> None:
    st.title("AI File Advisor")
    st.caption("先选择一个目录进行扫描。分析完成后，这里只展示用户真正需要的文件判断和处理建议。")
    st.info("在左侧输入目录路径并点击“扫描文件”。")


def _render_file_picker(scanned_files: list[dict[str, object]]) -> str:
    st.markdown("### 选择文件")
    selected_path = st.selectbox(
        "选择要分析的文件",
        options=[str(item["path"]) for item in scanned_files],
        format_func=lambda value: Path(value).name,
        index=_selected_index(scanned_files, st.session_state.get("selected_file")),
        label_visibility="collapsed",
    )
    st.session_state["selected_file"] = selected_path

    selected_item = _find_file(scanned_files, selected_path)
    with st.container(border=True):
        st.markdown(f"**{Path(selected_path).name}**")
        st.caption(str(selected_item.get("path", selected_path)))
        st.caption(f"已扫描 {len(scanned_files)} 个可分析文件")

    return selected_path


def _selected_index(scanned_files: list[dict[str, object]], selected_file: str | None) -> int:
    if not selected_file:
        return 0

    for index, item in enumerate(scanned_files):
        if item.get("path") == selected_file:
            return index
    return 0


def _find_file(scanned_files: list[dict[str, object]], selected_path: str) -> dict[str, object]:
    for item in scanned_files:
        if item.get("path") == selected_path:
            return item
    return {}


if __name__ == "__main__":
    main()

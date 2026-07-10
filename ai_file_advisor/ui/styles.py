from __future__ import annotations

import streamlit as st


def apply_app_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #f2f4f8;  /* 浅灰色背景 */
            color: #1f1f1f;       /* 深色文本 */
        }
        .block-container {
            max-width: 1180px;     /* 内容最大宽度 */
            padding-top: 2rem;
            padding-bottom: 2.4rem;
        }
        [data-testid="stSidebar"] {
            background: #ffffff;    /* 白色侧边栏 */
            border-right: 1px solid #e8ebf0;
        }
        h1, h2, h3 {
            letter-spacing: 0;
        }
        div[data-testid="stSelectbox"] > div {
            background: #ffffff;
        }
        .stButton > button {
            min-height: 2.6rem;
            background: #222222;   /* 深色按钮 */
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: 600;
        }
        .stButton > button:hover {
            background: #444444;  /* 悬停变亮 */
            color: white;
            border: none;
        }
        .stAlert {
            border-radius: 12px;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: #e7eaf0;
            border-radius: 18px;  /* 圆角容器 */
            background: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

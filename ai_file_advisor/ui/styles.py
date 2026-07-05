from __future__ import annotations

import streamlit as st


def apply_app_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #f2f4f8;
            color: #1f1f1f;
        }
        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 2.4rem;
        }
        [data-testid="stSidebar"] {
            background: #ffffff;
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
            background: #222222;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: 600;
        }
        .stButton > button:hover {
            background: #444444;
            color: white;
            border: none;
        }
        .stAlert {
            border-radius: 12px;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: #e7eaf0;
            border-radius: 18px;
            background: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

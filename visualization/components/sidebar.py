"""Компонент бокової панелі"""
import streamlit as st
from visualization.config.settings import DEFAULT_WEIGHTS
from visualization.utils.icons import get_icon


def render_sidebar():
    st.sidebar.markdown(
        f"<p style='color: #05e07e; font-size: 0.875rem; font-weight: 700; "
        f"text-transform: uppercase; letter-spacing: 0.1em; margin: 32px 0 16px 0;'>"
        f"{get_icon('settings', '#05e07e', '14px')} Налаштування</p>",
        unsafe_allow_html=True
    )
    weights = {'restaurants': st.sidebar.slider(
        "", 0.0, 1.0, DEFAULT_WEIGHTS['restaurants'], 0.05,
        key="restaurants", help="Вага ресторанів"
    )}
    st.sidebar.markdown(
        f"<p style='margin-top: -10px; color: #6b7280; font-size: 0.85rem;'>"
        f"{get_icon('restaurants', '#6b7280', '14px')} Ресторани</p>",
        unsafe_allow_html=True
    )
    weights['subway'] = st.sidebar.slider(
        "", 0.0, 1.0, DEFAULT_WEIGHTS['subway'], 0.05,
        key="subway", help="Вага метро"
    )
    st.sidebar.markdown(
        f"<p style='margin-top: -10px; color: #6b7280; font-size: 0.85rem;'>"
        f"{get_icon('subway', '#6b7280', '14px')} Метро</p>",
        unsafe_allow_html=True
    )
    weights['borough_quality'] = st.sidebar.slider(
        "", 0.0, 1.0, DEFAULT_WEIGHTS['borough_quality'], 0.05,
        key="borough_quality", help="Вага району"
    )
    st.sidebar.markdown(
        f"<p style='margin-top: -10px; color: #6b7280; font-size: 0.85rem;'>"
        f"{get_icon('borough_quality', '#6b7280', '14px')} Район</p>",
        unsafe_allow_html=True
    )

    return weights
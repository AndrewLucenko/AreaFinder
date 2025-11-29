"""Компонент легенди"""
import streamlit as st


def render_legend():
    st.sidebar.markdown("---")

    st.sidebar.markdown(
        "<p style='color: #05e07e; font-size: 0.875rem; font-weight: 700; "
        "text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px;'>"
        "<i class='fas fa-info-circle'></i> ШКАЛА ОЦІНКИ</p>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        "<p style='margin: 8px 0;'>"
        "<i class='fas fa-star' style='color: #05e07e;'></i> "
        "<span style='color: #e5e7eb;'>86-100: Відмінно</span>"
        "</p>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        "<p style='margin: 8px 0;'>"
        "<i class='fas fa-check-circle' style='color: #3b82f6;'></i> "
        "<span style='color: #e5e7eb;'>71-85: Добре</span>"
        "</p>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        "<p style='margin: 8px 0;'>"
        "<i class='fas fa-info-circle' style='color: #f59e0b;'></i> "
        "<span style='color: #e5e7eb;'>51-70: Середнє</span>"
        "</p>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        "<p style='margin: 8px 0;'>"
        "<i class='fas fa-times-circle' style='color: #ef4444;'></i> "
        "<span style='color: #e5e7eb;'>0-50: Низьке</span>"
        "</p>",
        unsafe_allow_html=True
    )
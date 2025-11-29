import streamlit as st
from visualization.utils.icons import get_icon


def render_header():
    st.markdown(f"""
        <div style='margin-bottom: 48px;'>
            <div style='display: flex; align-items: center; gap: 16px; margin-bottom: 12px;'>
                <div style='width: 64px; height: 64px; background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%); 
                            border-radius: 12px; display: flex; align-items: center; justify-content: center; 
                            border: 1px solid #3d3d3d;'>
                    {get_icon('map', '#05e07e', '28px')}
                </div>
                <h1 style='margin: 0;'>CitySpotter</h1>
            </div>
            <p style='color: #6b7280; font-size: 1.1rem; margin: 0; padding-left: 80px;'>
                Знайди ідеальне місце для події в Нью-Йорку
            </p>
        </div>
    """, unsafe_allow_html=True)
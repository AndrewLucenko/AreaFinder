"""Компонент списку локацій"""
import streamlit as st
from visualization.utils.scoring import get_status, get_gradient_by_value, get_color_by_value

def render_progress_bar(value, max_value=1):
    percentage = (value / max_value) * 100
    print(percentage)
    color, _ = get_color_by_value(value, max_value)

    if color == '#05e07e':
        gradient = 'linear-gradient(90deg, #05e07e 0%, #00ff88 100%)'
    elif color == '#3b82f6':
        gradient = 'linear-gradient(90deg, #3b82f6 0%, #2563eb 100%)'
    elif color == '#f59e0b':
        gradient = 'linear-gradient(90deg, #f59e0b 0%, #d97706 100%)'
    else:
        gradient = 'linear-gradient(90deg, #ef4444 0%, #dc2626 100%)'

    return f"""
        <div style='background: #1a1a1a; border-radius: 12px; height: 8px; 
                    overflow: hidden; margin: 2px 0 4px 0; border: 1px solid #2d2d2d;'>
            <div style='background: {gradient}; height: 100%; width: {percentage}%; 
                        border-radius: 12px; transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
                        box-shadow: 0 0 12px {color}80;'></div>
        </div>
    """


def render_location_list(locations):
    st.markdown(
        "<h2><i class='fas fa-trophy' style='color: #05e07e; margin-right: 12px;'></i>"
        "Рейтинг локацій</h2>",
        unsafe_allow_html=True
    )

    for i, loc in enumerate(locations):
        score = loc.get('score', 0)
        print(score)
        name = loc.get('name', 'Unknown')
        normalized = loc.get('normalized', {})

        restaurants_val = normalized.get('restaurants', 0)
        subway_val = normalized.get('subway', 0)
        borough_quality_val = normalized.get('borough_quality', 0)

        status = get_status(score)
        score_gradient = get_gradient_by_value(score, 1)

        with st.expander(f"#{i + 1} {name} • {score:.2f}"):
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown(f"""
                    <div style='text-align: center; padding: 24px; 
                                background: {score_gradient}; 
                                border-radius: 16px; color: #000;'>
                        <div style='font-size: 3rem; font-weight: 900;'>{score:.2f}</div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)

                badge_gradient = get_gradient_by_value(score, 1)
                st.markdown(f"""
                    <div style='text-align: center;'>
                        <span style='padding: 6px 16px; border-radius: 20px; 
                                     font-size: 0.8rem; font-weight: 700; 
                                     background: {badge_gradient}; 
                                     color: #000; display: inline-block;
                                     margin-bottom: 14px;'>
                            {status["text"]}
                        </span>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                metrics = [
                    ("🍴 Ресторани", restaurants_val),
                    ("🚇 Метро", subway_val),
                    ("🏙 Район", borough_quality_val)
                ]

                metrics_html = ""
                for label, value in metrics:
                    color, _ = get_color_by_value(value)

                    metrics_html += f"""
                        <div style='margin-bottom: 16px;'>
                            <div style='font-weight: 600; color: #e5e7eb; margin-bottom: 4px; font-size: 0.9rem;'>
                                {label}
                            </div>
                            <div style='background: #1a1a1a; border-radius: 12px; height: 8px; 
                                        overflow: hidden; margin: 2px 0 4px 0; border: 1px solid #2d2d2d;'>
                                <div style='background: {get_gradient_by_value(value, 1)}; height: 100%; 
                                            width: {value * 100}%; border-radius: 12px; 
                                            transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
                                            box-shadow: 0 0 12px {color}80;'></div>
                            </div>
                            <div style='color: {color}; font-weight: 700; margin-top: 2px; font-size: 0.95rem;'>
                                {value:.2f}
                            </div>
                        </div>
                    """

                st.markdown(metrics_html, unsafe_allow_html=True)

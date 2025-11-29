"""Компонент топ-метрик"""
import streamlit as st
from visualization.utils.scoring import get_best_metric
from scripts.get_description import get_place_description


def render_top_metrics(locations):
    st.markdown("<br>", unsafe_allow_html=True)

    if not locations:
        return

    best = locations[0]
    best_name = best['name']
    best_score = best['score']

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("НАЙКРАЩА ЛОКАЦІЯ", best_name)

    with col2:
        st.metric("НАЙВИЩИЙ БАЛ", f"{best_score:.1f}")

    with col3:
        st.metric("СИЛЬНА СТОРОНА", get_best_metric(best))

    st.markdown("<br>", unsafe_allow_html=True)

    state_key = f'ai_desc_top_{best_name.replace(" ", "_")}'

    if state_key not in st.session_state:
        st.session_state[state_key] = None

    button_key = f'btn_top_{best_name.replace(" ", "_")}'

    col_btn, col_empty = st.columns([1, 3])

    with col_btn:
        button_clicked = st.button(
            "🤖 AI опис найкращої локації",
            key=button_key,
            use_container_width=True
        )

    if button_clicked:
        progress_placeholder = st.empty()
        with progress_placeholder:
            with st.spinner('⏳ Генерую детальний опис...'):
                description = get_place_description(best_name, best_score)
                st.session_state[state_key] = description
                print(f"✅ Згенеровано опис для {best_name}: {description[:50]}...")

        progress_placeholder.empty()

    if st.session_state[state_key]:
        st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
                        padding: 20px; border-radius: 12px; border: 1px solid #2d2d2d;
                        font-size: 1rem; line-height: 1.8; color: #e5e7eb;
                        box-shadow: 0 4px 16px rgba(5, 224, 126, 0.1);'>
                <div style='color: #05e07e; font-weight: 700; margin-bottom: 8px; font-size: 0.9rem;'>
                    📍 {best_name}
                </div>
                {st.session_state[state_key]}
            </div>
        """, unsafe_allow_html=True)

        print(f"✅ Показую збережений опис для {best_name}")
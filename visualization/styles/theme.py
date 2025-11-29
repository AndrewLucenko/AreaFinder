import streamlit as st


def apply_theme():
    css = """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* === GLOBAL === */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background: #000000;
        }

        /* === SIDEBAR === */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);
            border-right: 1px solid #2d2d2d;
        }

        /* === TYPOGRAPHY === */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        h1 {
            font-size: 3rem !important;
            background: linear-gradient(135deg, #ffffff 0%, #b0b0b0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        p, span, label, div {
            color: #e5e7eb !important;
        }

        /* === SLIDERS === */
        .stSlider > div > div > div > div {
            background-color: #05e07e !important;
        }

        .stSlider > div > div > div {
            background: #2d2d2d !important;
        }

        /* Приховати hover підказки на слайдері */
        .stSlider [data-baseweb="tooltip"] {
            display: none !important;
        }

        /* Приховати tick values під слайдером */
        .stSlider > div > div > div > div[data-testid] > div[role="slider"] + div {
            display: none !important;
        }

        /* Приховати всі tick marks */
        .stSlider [role="presentation"] {
            display: none !important;
        }

        /* === METRICS === */
        [data-testid="stMetricValue"] {
            color: #05e07e !important;
            font-size: 2.5rem !important;
            font-weight: 800 !important;
        }

        [data-testid="stMetricLabel"] {
            color: #6b7280 !important;
            font-size: 0.75rem !important;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
        }

        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
            padding: 24px;
            border-radius: 16px;
            border: 1px solid #2d2d2d;
            transition: all 0.3s ease;
        }

        div[data-testid="metric-container"]:hover {
            border-color: #05e07e;
            box-shadow: 0 8px 32px rgba(5, 224, 126, 0.2);
            transform: translateY(-4px);
        }

        /* === EXPANDER === */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%) !important;
            border: 1px solid #2d2d2d !important;
            border-radius: 16px !important;
            padding: 20px !important;
            color: #ffffff !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin: 12px 0 !important;
        }

        .streamlit-expanderHeader:hover {
            border-color: #05e07e !important;
            background: linear-gradient(135deg, #232323 0%, #1a1a1a 100%) !important;
            transform: translateX(4px);
            box-shadow: 0 8px 32px rgba(5, 224, 126, 0.15);
        }

        .streamlit-expanderContent {
            background: #0a0a0a !important;
            border: 1px solid #2d2d2d !important;
            border-top: none !important;
            border-radius: 0 0 16px 16px !important;
            padding: 24px !important;
        }

        /* === DIVIDER === */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, #2d2d2d 50%, transparent 100%);
            margin: 48px 0;
        }
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)


# Додаткові компонентні стилі
COMPONENT_STYLES = {
    "icon_box": """
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #3d3d3d;
    """,

    "score_badge": """
        background: linear-gradient(135deg, #05e07e 0%, #00d97e 100%);
        color: #000000;
        font-size: 3rem;
        font-weight: 900;
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(5, 224, 126, 0.4);
    """,

    "progress_container": """
        background: #1a1a1a;
        border-radius: 12px;
        height: 12px;
        overflow: hidden;
        margin: 8px 0;
        border: 1px solid #2d2d2d;
    """,

    "progress_bar": """
        background: linear-gradient(90deg, #05e07e 0%, #00ff88 100%);
        height: 100%;
        border-radius: 12px;
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 20px rgba(5, 224, 126, 0.5);
    """,

    "metric_row": """
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px;
        margin: 8px 0;
        background: #0a0a0a;
        border-radius: 12px;
        border: 1px solid #1a1a1a;
        transition: all 0.3s ease;
    """,

    "legend_box": """
        background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
        border: 1px solid #2d2d2d;
        border-radius: 16px;
        padding: 20px;
        margin-top: 24px;
    """,

    "legend_item": """
        display: flex;
        align-items: center;
        padding: 12px;
        margin: 8px 0;
        background: #0a0a0a;
        border-radius: 8px;
        transition: all 0.3s ease;
    """
}
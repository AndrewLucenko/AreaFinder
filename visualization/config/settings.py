"""Налаштування додатку"""

# Конфігурація сторінки
PAGE_CONFIG = {
    "page_title": "CitySpotter",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Дефолтні ваги
DEFAULT_WEIGHTS = {
    "restaurants": 0.5,
    "subway": 0.5,
    "borough_quality": 0.1
}

# Параметри карти
MAP_CONFIG = {
    "center": [40.7128, -74.0060],  # NYC
    "zoom": 13,  # ✅ Було 11, стало 13 (більше zoom)
    "tile": "CartoDB dark_matter"
}

# Пороги для оцінки
SCORE_THRESHOLDS = {
    "excellent": 0.86,
    "good": 0.71,
    "average": 0.51
}

# Статуси
STATUSES = {
    "excellent": {
        "color": "green",
        "text": "EXCELLENT",
        "class": "status-excellent",
        "icon": "fa-star"
    },
    "good": {
        "color": "lightblue",
        "text": "GOOD",
        "class": "status-good",
        "icon": "fa-check-circle"
    },
    "average": {
        "color": "orange",
        "text": "AVERAGE",
        "class": "status-average",
        "icon": "fa-info-circle"
    },
    "poor": {
        "color": "red",
        "text": "POOR",
        "class": "status-poor",
        "icon": "fa-times-circle"
    }
}
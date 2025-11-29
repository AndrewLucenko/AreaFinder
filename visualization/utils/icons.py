"""Іконки та їх конфігурація"""

ICONS = {
    # Метрики (оновлені)
    "restaurants": "fa-utensils",
    "subway": "fa-subway",

    # UI елементи
    "map": "fa-map-marked-alt",
    "trophy": "fa-trophy",
    "marker": "fa-map-marker-alt",
    "settings": "fa-sliders-h",
    "info": "fa-info-circle",

    # Статуси
    "star": "fa-star",
    "check": "fa-check-circle",
    "warning": "fa-info-circle",
    "error": "fa-times-circle"
}


def get_icon(name, color="#05e07e", size="16px"):
    """Отримати HTML іконки"""
    icon_class = ICONS.get(name, "fa-circle")
    return f'<i class="fas {icon_class}" style="color: {color}; font-size: {size};"></i>'


def icon(name):
    """Швидкий доступ до класу іконки"""
    return ICONS.get(name, "fa-circle")
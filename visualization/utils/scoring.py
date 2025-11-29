"""Розрахунок балів та статусів"""
from visualization.config.settings import SCORE_THRESHOLDS, STATUSES

def sort_by_score(locations):
    return sorted(locations, key=lambda x: x['score'], reverse=True)


def get_status(score):
    if score >= SCORE_THRESHOLDS['excellent']:
        return STATUSES['excellent']
    elif score >= SCORE_THRESHOLDS['good']:
        return STATUSES['good']
    elif score >= SCORE_THRESHOLDS['average']:
        return STATUSES['average']
    else:
        return STATUSES['poor']


def get_color_by_value(value, max_value=1):
    normalized = (value / max_value) * 100

    if normalized >= 86:
        return '#05e07e', 'green'
    elif normalized >= 71:
        return '#3b82f6', 'blue'
    elif normalized >= 51:
        return '#f59e0b', 'orange'
    else:
        return '#ef4444', 'red'


def get_gradient_by_value(value, max_value=1):
    color, _ = get_color_by_value(value, max_value)

    if color == '#05e07e':
        return 'linear-gradient(135deg, #05e07e 0%, #00d97e 100%)'
    elif color == '#3b82f6':
        return 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
    elif color == '#f59e0b':
        return 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
    else:
        return 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)'


def get_best_metric(location):
    restaurants_val = location.get('normalized', {}).get('restaurants', location.get('restaurants', 0))
    subway_val = location.get('subway', 0)
    borough_val = location.get('borough_quality', 0)

    metrics = {
        'restaurants': ('Ресторани', restaurants_val),
        'subway': ('Метро', subway_val),
        'borough_quality': ('Якість району', borough_val)
    }

    best_key = max(metrics.keys(), key=lambda k: metrics[k][1])

    return metrics[best_key][0]
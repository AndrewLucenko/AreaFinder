"""Тестові дані"""

def get_locations():
    return [
        {
            "name": "Central Park South",
            "lat": 40.7678,
            "lon": -73.9812,
            "transport": 9.2,
            "social": 8.5,
            "space": 9.8,
            "balance": 7.1
        },
        {
            "name": "Brooklyn Bridge Park",
            "lat": 40.7024,
            "lon": -73.9964,
            "transport": 7.8,
            "social": 9.1,
            "space": 8.7,
            "balance": 8.2
        },
        {
            "name": "Union Square",
            "lat": 40.7359,
            "lon": -73.9911,
            "transport": 9.5,
            "social": 8.9,
            "space": 6.2,
            "balance": 7.8
        },
        {
            "name": "Prospect Park",
            "lat": 40.6602,
            "lon": -73.9690,
            "transport": 7.1,
            "social": 7.8,
            "space": 9.5,
            "balance": 8.1
        },
        {
            "name": "Bryant Park",
            "lat": 40.7536,
            "lon": -73.9832,
            "transport": 8.9,
            "social": 8.4,
            "space": 7.2,
            "balance": 7.5
        },
        {
            "name": "Times Square",
            "lat": 40.7580,
            "lon": -73.9855,
            "transport": 5.2,
            "social": 4.1,
            "space": 3.5,
            "balance": 4.8
        }
    ]


def load_from_json(filepath):
    import json
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data.get('locations', [])


def load_from_csv(filepath):
    import pandas as pd
    df = pd.read_csv(filepath)
    return df.to_dict('records')
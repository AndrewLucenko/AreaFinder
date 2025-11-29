import json
import os

from scripts.score_algorithm import filter_locations, add_normalized_fields
from scripts.get_description import get_place_description
viewport = {
    "ne_lat": 40.80,
    "ne_lng": -73.90,
    "sw_lat": 40.70,
    "sw_lng": -74.10
}

weights = {
    "restaurants": 0.6,
    "subway": 0.3,
    "borough_quality": 0.1
}

add_normalized_fields('data/processed/merged_data.json', 'data/processed')

with open('data/processed/merged_data_normalized.json', 'r') as f:
    normalized_data = json.load(f)

result = filter_locations(normalized_data, viewport, weights, min_score=0.5)


# desc = get_place_description("Bryant Park", 0.93)
# print(desc)

def main():
    print(result)


if __name__ == "__main__":
    main()

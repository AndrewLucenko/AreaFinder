import json
import os

def add_normalized_fields(input_path, output_dir):
    with open(input_path, "r") as f:
        data = json.load(f)

    restaurants_vals = [d["restaurants_nearby"] for d in data]
    subway_vals = [d["subway_stations_nearby"] for d in data]

    min_rest, max_rest = min(restaurants_vals), max(restaurants_vals)
    min_sub, max_sub = min(subway_vals), max(subway_vals)

    rest_range = max_rest - min_rest if max_rest != min_rest else 1
    sub_range = max_sub - min_sub if max_sub != min_sub else 1

    borough_scores = {
        "Manhattan": 1.0,
        "Brooklyn": 0.8,
        "Queens": 0.6,
        "Bronx": 0.3,
        "Staten Island": 0.2
    }

    for d in data:
        restaurants_norm = (d["restaurants_nearby"] - min_rest) / rest_range
        subway_norm = (d["subway_stations_nearby"] - min_sub) / sub_range

        borough = d.get("borough")
        borough_quality = borough_scores.get(borough, 0.5)  # default 0.5 якщо район невідомий

        d["normalized"] = {
            "restaurants": restaurants_norm,
            "subway": subway_norm,
            "borough_quality": borough_quality
        }

    new_filename = os.path.splitext(os.path.basename(input_path))[0] + "_normalized.json"
    output_path = os.path.join(output_dir, new_filename)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    return data

def filter_locations(data, viewport, weights, min_score=0.0):
    """
    Повертає JSON з локаціями, які:
    1) знаходяться у межах видимої частини карти (viewport)
    2) мають score >= min_score
    3) вже містять усі normalized коефіцієнти + score

    viewport = {
        "ne_lat": ...,
        "ne_lng": ...,
        "sw_lat": ...,
        "sw_lng": ...
    }

    weights = {
        "restaurants": 0.6,
        "subway": 0.3,
        "borough_quality": 0.1
    }
    """

    ne_lat = viewport["ne_lat"]
    ne_lng = viewport["ne_lng"]
    sw_lat = viewport["sw_lat"]
    sw_lng = viewport["sw_lng"]

    w_rest = weights.get("restaurants", 0.6)
    w_sub = weights.get("subway", 0.3)
    w_bor = weights.get("borough_quality", 0.1)

    filtered = []

    for d in data:
        lat = d["latitude"]
        lng = d["longitude"]

        if not (sw_lat <= lat <= ne_lat and sw_lng <= lng <= ne_lng):
            continue

        rest_n = d["normalized"]["restaurants"]
        sub_n = d["normalized"]["subway"]
        bor_n = d["normalized"]["borough_quality"]

        score = (
            w_rest * rest_n +
            w_sub * sub_n +
            w_bor * bor_n
        )

        d["score"] = round(score, 4)

        if score >= min_score:
            filtered.append(d)

    filtered.sort(key=lambda x: x["score"], reverse=True)

    return {
        "count": len(filtered),
        "locations": filtered
    }


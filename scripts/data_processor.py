import json
import time
import numpy as np
from pathlib import Path
from typing import List, Dict
from sklearn.neighbors import BallTree

def load_parks_json() -> List[Dict]:
    print("Loading parks...")

    borough_map = {'B': 'Brooklyn', 'M': 'Manhattan', 'Q': 'Queens', 'R': 'Staten Island', 'X': 'Bronx'}

    try:
        with open(Path("data/raw/parks.json")) as f:
            parks_data = json.load(f)

        for record in parks_data:
            if record.get('borough') in borough_map:
                record['borough'] = borough_map[record['borough']]

        print(f"  ✓ Loaded {len(parks_data)} parks")
        return parks_data

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []

def load_restaurants_json() -> List[Dict]:
    print("Loading restaurants...")

    try:
        with open(Path("data/raw/restaurants.json")) as f:
            restaurants_data = json.load(f)

        print(f"  ✓ Loaded {len(restaurants_data)} restaurants")
        return restaurants_data

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []

def load_subway_json() -> List[Dict]:
    print("Loading subway...")

    try:
        with open(Path("data/raw/subway.json")) as f:
            subway_data = json.load(f)

        print(f"  ✓ Loaded {len(subway_data)} subway stations")
        return subway_data

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []

def add_proximity_info(parks: List[Dict], restaurants: List[Dict], subway: List[Dict], radius_km: float = 0.8) -> List[Dict]:
    print(f"\nCalculating proximity (radius: {radius_km} km)...")
    print(f"  Parks to process: {len(parks)}")
    print(f"  Restaurants to search: {len(restaurants)}")
    print(f"  Subway stations to search: {len(subway)}")

    radius_rad = radius_km / 6371

    parks_coords = np.radians(np.array([[float(park['latitude']), float(park['longitude'])] for park in parks]))

    if len(restaurants) > 0:
        restaurants_coords = np.radians(np.array([[float(restaurant['latitude']), float(restaurant['longitude'])] for restaurant in restaurants]))
        restaurants_tree = BallTree(restaurants_coords, metric='haversine')
    else:
        restaurants_tree = None

    if len(subway) > 0:
        subway_coords = np.radians(np.array([[float(station['latitude']), float(station['longitude'])] for station in subway]))
        subway_tree = BallTree(subway_coords, metric='haversine')
    else:
        subway_tree = None

    for i, park in enumerate(parks):
        park_coord = parks_coords[i:i+1]

        if restaurants_tree is not None:
            restaurant_indices = restaurants_tree.query_radius(park_coord, r=radius_rad)[0]
            park['restaurants_nearby'] = len(restaurant_indices)
        else:
            park['restaurants_nearby'] = 0

        if subway_tree is not None:
            subway_indices = subway_tree.query_radius(park_coord, r=radius_rad)[0]
            park['subway_stations_nearby'] = len(subway_indices)
        else:
            park['subway_stations_nearby'] = 0

        if (i + 1) % 500 == 0:
            progress_pct = ((i + 1) / len(parks)) * 100
            print(f"  Progress: {i + 1}/{len(parks)} ({progress_pct:.1f}%)")

    print(f"  ✓ Proximity calculated for all {len(parks)} parks")
    return parks

def save_results(parks: List[Dict]):
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    if len(parks) == 0:
        print("No parks to save")
        return None

    json_path = output_dir / "merged_data.json"
    with open(json_path, 'w') as f:
        json.dump(parks, f, indent=2)
    print(f"\n✓ JSON saved: {json_path}")

    print("\n" + "="*50)
    print("📊 Parks Statistics:")
    print(f"  Total parks: {len(parks)}")
    print("="*50)

    return parks

if __name__ == "__main__":
    start_time = time.time()
    print("Starting data processing...\n")

    parks = load_parks_json()
    restaurants = load_restaurants_json()
    subway = load_subway_json()

    if len(parks) > 0:
        parks = add_proximity_info(parks, restaurants, subway)

        df = save_results(parks)

        print("\n✅ Data processing completed!")
    else:
        print("❌ No parks found to process")

    elapsed = time.time() - start_time
    print(f"\n⏱️  Total time: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")

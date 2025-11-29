import requests
import json
import os
from pathlib import Path

# API endpoints (oData v4)
PARKS_API = "https://data.cityofnewyork.us/api/odata/v4/enfh-gkve"
RESTAURANTS_API = "https://data.cityofnewyork.us/api/odata/v4/43nn-pn8j"
SUBWAY_API = "https://data.ny.gov/api/odata/v4/39hk-dx4f"

LIMIT = 50000

def create_output_dir():
    output_dir = Path(__file__).parent.parent/"data"/"raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def load_parks():
    print("📍 Loading parks data...")
    borough_map = {'B': 'Brooklyn', 'M': 'Manhattan', 'Q': 'Queens', 'R': 'Staten Island', 'X': 'Bronx'}

    try:
        params = {"$top": LIMIT}
        response = requests.get(PARKS_API, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        venues = []

        for park_record in data.get('value', []):
            if park_record.get('multipolygon') and park_record.get('name311'):
                multipolygon = park_record['multipolygon']
                if multipolygon.get('coordinates') and len(multipolygon['coordinates']) > 0:
                    coords = multipolygon['coordinates'][0][0]
                    if coords and len(coords) > 0:
                        lon_sum = sum(coordinate[0] for coordinate in coords)
                        lat_sum = sum(coordinate[1] for coordinate in coords)
                        centroid_lon = lon_sum / len(coords)
                        centroid_lat = lat_sum / len(coords)

                        borough_code = park_record.get('borough')
                        borough_name = borough_map.get(borough_code, borough_code)

                        venues.append({
                            'name': park_record.get('name311'),
                            'borough': borough_name,
                            'latitude': centroid_lat,
                            'longitude': centroid_lon
                        })

        output_dir = create_output_dir()
        output_file = output_dir / "parks.json"

        with open(output_file, 'w') as f:
            json.dump(venues, f, indent=2)

        print(f"✓ Parks: {len(venues)} records saved to {output_file}")
        return True

    except Exception as e:
        print(f"❌ Error loading parks: {e}")
        return False

def load_restaurants():
    print("🍽️  Loading restaurant data...")
    try:
        params = {"$top": LIMIT}
        response = requests.get(RESTAURANTS_API, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        venues = []
        for restaurant_record in data.get('value', []):
            if restaurant_record.get('latitude') and restaurant_record.get('longitude'):
                venues.append({
                    'name': restaurant_record.get('dba', 'Unknown'),
                    'latitude': restaurant_record.get('latitude'),
                    'longitude': restaurant_record.get('longitude')
                })

        output_dir = create_output_dir()
        output_file = output_dir / "restaurants.json"

        with open(output_file, 'w') as f:
            json.dump(venues, f, indent=2)

        print(f"✓ Restaurants: {len(venues)} records saved to {output_file}")
        return True

    except Exception as e:
        print(f"❌ Error loading restaurants: {e}")
        return False

def load_subway():
    print("🚇 Loading subway data...")
    try:
        params = {"$top": LIMIT}
        response = requests.get(SUBWAY_API, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        venues = []
        for subway_record in data.get('value', []):
            if subway_record.get('gtfs_latitude') and subway_record.get('gtfs_longitude'):
                venues.append({
                    'name': subway_record.get('stop_name', 'Unknown'),
                    'latitude': subway_record.get('gtfs_latitude'),
                    'longitude': subway_record.get('gtfs_longitude')
                })

        output_dir = create_output_dir()
        output_file = output_dir / "subway.json"

        with open(output_file, 'w') as f:
            json.dump(venues, f, indent=2)

        print(f"✓ Subway: {len(venues)} records saved to {output_file}")
        return True

    except Exception as e:
        print(f"❌ Error loading subway: {e}")
        return False

if __name__ == "__main__":
    print("Starting data download...\n")

    results = {
        'parks': load_parks(),
        'restaurants': load_restaurants(),
        'subway': load_subway()
    }

    print("\n" + "="*50)
    if all(results.values()):
        print("✅ All datasets downloaded successfully!")
    else:
        print("⚠️ Some datasets failed to download")
        for dataset, success in results.items():
            status = "✓" if success else "✗"
            print(f"  {status} {dataset}")

"""Генератор тестових даних для NYC"""
import json
import random
import os

# Межі NYC (приблизні координати)
NYC_BOUNDS = {
    'lat_min': 40.4774,  # Південна межа
    'lat_max': 40.9176,  # Північна межа
    'lon_min': -74.2591,  # Західна межа
    'lon_max': -73.7004  # Східна межа
}

# Шаблони назв локацій
LOCATION_TEMPLATES = [
    "{street} & {avenue}",
    "{park} Park",
    "{street} Plaza",
    "{avenue} Square",
    "{area} Commons",
    "{street} Garden",
    "{area} Center",
    "{park} Field",
    "{street} Station Area",
    "{avenue} Hub"
]

STREETS = [
    "1st", "2nd", "3rd", "5th", "7th", "10th", "14th", "23rd", "34th", "42nd",
    "59th", "72nd", "86th", "96th", "110th", "125th", "145th", "168th",
    "Broadway", "Amsterdam", "Columbus", "Lexington", "Madison", "Park",
    "Wall", "Canal", "Houston", "Spring", "Prince", "Bleecker", "West",
    "East", "Worth", "Grand", "Delancey", "Rivington", "Stanton"
]

AVENUES = [
    "1st Ave", "2nd Ave", "3rd Ave", "5th Ave", "6th Ave", "7th Ave",
    "8th Ave", "9th Ave", "10th Ave", "11th Ave", "Amsterdam Ave",
    "Columbus Ave", "Lexington Ave", "Madison Ave", "Park Ave",
    "Broadway", "West End Ave", "Riverside Dr"
]

PARKS = [
    "Central", "Prospect", "Bryant", "Madison", "Washington",
    "Tompkins", "Union", "McCarren", "Fort Greene", "Sunset",
    "Riverside", "Carl Schurz", "Morningside", "St Nicholas",
    "Marcus Garvey", "Herbert Von King", "Brooklyn Bridge"
]

AREAS = [
    "Chelsea", "SoHo", "TriBeCa", "NoHo", "FiDi", "Murray Hill",
    "Gramercy", "Kips Bay", "Midtown", "Hell's Kitchen", "Harlem",
    "Williamsburg", "Greenpoint", "Bushwick", "DUMBO", "Park Slope",
    "Carroll Gardens", "Red Hook", "Gowanus", "Sunset Park",
    "Bay Ridge", "Bensonhurst", "Crown Heights", "Bedford-Stuyvesant",
    "Fort Greene", "Clinton Hill", "Prospect Heights", "Cobble Hill",
    "Boerum Hill", "Downtown Brooklyn", "Brooklyn Heights"
]


def generate_random_location(index):
    """Згенерувати одну випадкову локацію"""

    # Випадкові координати в межах NYC
    lat = random.uniform(NYC_BOUNDS['lat_min'], NYC_BOUNDS['lat_max'])
    lon = random.uniform(NYC_BOUNDS['lon_min'], NYC_BOUNDS['lon_max'])

    # Випадкова назва
    template = random.choice(LOCATION_TEMPLATES)
    name = template.format(
        street=random.choice(STREETS),
        avenue=random.choice(AVENUES),
        park=random.choice(PARKS),
        area=random.choice(AREAS)
    )

    # Додати номер якщо дублікат (простий підхід)
    if random.random() < 0.3:  # 30% шанс додати номер
        name = f"{name} #{random.randint(1, 5)}"

    # Випадкові метрики з реалістичним розподілом
    # Використовуємо нормальний розподіл з центром 6.5
    transport = max(0, min(10, random.gauss(6.5, 2.0)))
    social = max(0, min(10, random.gauss(6.5, 2.0)))
    space = max(0, min(10, random.gauss(6.0, 2.5)))
    balance = max(0, min(10, random.gauss(7.0, 1.5)))

    return {
        "name": name,
        "lat": round(lat, 6),
        "lon": round(lon, 6),
        "transport": round(transport, 1),
        "social": round(social, 1),
        "space": round(space, 1),
        "balance": round(balance, 1)
    }


def generate_dataset(num_locations=10000):
    """Згенерувати повний датасет"""

    print(f"🔄 Генерація {num_locations:,} локацій...")

    locations = []

    # Додати кілька "gold standard" локацій з високими балами
    premium_locations = [
        {
            "name": "Central Park South & 5th Ave",
            "lat": 40.7678,
            "lon": -73.9812,
            "transport": 9.2,
            "social": 8.5,
            "space": 9.8,
            "balance": 7.1
        },
        {
            "name": "Brooklyn Bridge Park Pier 1",
            "lat": 40.7024,
            "lon": -73.9964,
            "transport": 7.8,
            "social": 9.1,
            "space": 8.7,
            "balance": 8.2
        },
        {
            "name": "Union Square Park",
            "lat": 40.7359,
            "lon": -73.9911,
            "transport": 9.5,
            "social": 8.9,
            "space": 6.2,
            "balance": 7.8
        },
        {
            "name": "Prospect Park Long Meadow",
            "lat": 40.6602,
            "lon": -73.9690,
            "transport": 7.1,
            "social": 7.8,
            "space": 9.5,
            "balance": 8.1
        },
        {
            "name": "Bryant Park Main Lawn",
            "lat": 40.7536,
            "lon": -73.9832,
            "transport": 8.9,
            "social": 8.4,
            "space": 7.2,
            "balance": 7.5
        }
    ]

    locations.extend(premium_locations)

    # Згенерувати решту локацій
    for i in range(num_locations - len(premium_locations)):
        locations.append(generate_random_location(i))

        # Показати прогрес
        if (i + 1) % 1000 == 0:
            print(f"  ✓ Згенеровано {i + 1:,} локацій...")

    print(f"✅ Згенеровано {len(locations):,} локацій")

    return locations


def save_to_output(locations, filename='locations.json'):
    """Зберегти в output папку"""

    # Створити output папку якщо не існує
    os.makedirs('output', exist_ok=True)

    output_data = {
        "locations": locations,
        "metadata": {
            "total": len(locations),
            "generated_by": "generate_test_data.py",
            "description": "Test dataset for NYC event locations"
        }
    }

    filepath = os.path.join('output', filename)

    print(f"💾 Збереження в {filepath}...")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    # Показати розмір файлу
    file_size = os.path.getsize(filepath)
    size_mb = file_size / (1024 * 1024)

    print(f"✅ Збережено! Розмір файлу: {size_mb:.2f} MB")

    # Статистика
    print(f"\n📊 Статистика:")
    print(f"  Всього локацій: {len(locations):,}")

    # Середні значення метрик
    avg_transport = sum(loc['transport'] for loc in locations) / len(locations)
    avg_social = sum(loc['social'] for loc in locations) / len(locations)
    avg_space = sum(loc['space'] for loc in locations) / len(locations)
    avg_balance = sum(loc['balance'] for loc in locations) / len(locations)

    print(f"  Середні метрики:")
    print(f"    Транспорт: {avg_transport:.2f}")
    print(f"    Соц. активність: {avg_social:.2f}")
    print(f"    Простір: {avg_space:.2f}")
    print(f"    Баланс: {avg_balance:.2f}")


def main():
    """Головна функція"""

    print("🗽 CitySpotter - Генератор тестових даних для NYC\n")

    # Можна змінити кількість
    num_locations = 10000  # Зміни це число для більше/менше локацій

    # Згенерувати
    locations = generate_dataset(num_locations)

    # Зберегти
    save_to_output(locations)

    print("\n🎉 Готово! Тепер можна запустити додаток:")
    print("   python -m streamlit run main.py")


if __name__ == "__main__":
    main()
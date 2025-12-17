import requests
import json

# Test the route endpoint
url = "http://localhost:8000/api/navigation/simple-route"

params = {
    "start_lat": 41.0181602,
    "start_lon": 28.9107131,
    "end_lat": 41.0309288,
    "end_lon": 29.0987145,
    "vehicle_range_km": 255,
    "battery_capacity_kwh": 50,
    "current_battery_percent": 80,
    "min_charge_percent": 20,
    "preferred_charge_percent": 80,
}

print("Testing route endpoint...")
print(f"URL: {url}")
print(f"Params: {json.dumps(params, indent=2)}")

try:
    response = requests.post(url, params=params, timeout=30)
    print(f"\nStatus Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("\nRoute Data:")
        print(f"- Success: {data.get('success')}")
        print(f"- Message: {data.get('message')}")

        if "route_summary" in data:
            summary = data["route_summary"]
            print(f"\nRoute Summary:")
            print(f"  - Distance: {summary.get('total_distance_km')} km")
            print(f"  - Driving time: {summary.get('driving_time_minutes')} min")
            print(f"  - With traffic: {summary.get('with_traffic')}")
            print(f"  - Traffic delay: {summary.get('traffic_delay_minutes')} min")

        if "route_coordinates" in data:
            coords = data["route_coordinates"]
            print(f"\nRoute Coordinates:")
            print(f"  - Total points: {len(coords)}")
            print(f"  - First 3 points: {coords[:3]}")
            print(f"  - Last 3 points: {coords[-3:]}")

            # Check if it's a straight line (only 2 points) or detailed route
            if len(coords) == 2:
                print("  WARNING: Only 2 points - this is a straight line!")
            else:
                print(f"  Good: {len(coords)} detailed route points from TomTom")
    else:
        print("Request failed")
        print(response.text)

except Exception as e:
    print(f"Exception: {e}")

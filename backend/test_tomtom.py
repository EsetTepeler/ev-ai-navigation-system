import requests
import json

TOMTOM_API_KEY = "NilqB0Tl3r0T1dMLMx277kjXS6d0IY4s"
TOMTOM_ROUTING_API = "https://api.tomtom.com/routing/1/calculateRoute/"


def test_tomtom():
    # Istanbul coordinates (approx)
    start_lat, start_lon = 41.0082, 28.9784
    end_lat, end_lon = 41.0422, 29.0067  # Besiktas

    locations = f"{start_lat},{start_lon}:{end_lat},{end_lon}"
    url = f"{TOMTOM_ROUTING_API}{locations}/json"

    params = {
        "key": TOMTOM_API_KEY,
        "traffic": "true",
        "routeType": "fastest",
        "travelMode": "car",
        "vehicleEngineType": "electric",
    }

    print(f"Testing TomTom API...")
    print(f"URL: {url}")

    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if "routes" in data and len(data["routes"]) > 0:
                summary = data["routes"][0]["summary"]
                print("Success! Route found.")
                print(f"Distance: {summary.get('lengthInMeters')} meters")
                print(f"Time: {summary.get('travelTimeInSeconds')} seconds")
                print(f"Traffic Delay: {summary.get('trafficDelayInSeconds')} seconds")
            else:
                print("Response 200 but no routes found.")
                print(json.dumps(data, indent=2))
        else:
            print("API Request Failed")
            print(response.text)

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    test_tomtom()

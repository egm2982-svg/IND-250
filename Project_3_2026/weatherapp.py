# first install requests -> pip install requests
import json

import requests

def get_weather_by_city(city, state):
    # 1. Geocoding API: Convert City/State to Coordinates
    # We combine city and state in the 'name' parameter for better accuracy

    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&admin1={state}&count=10&language=en&format=json"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()

    if "results" not in geo_data:
        print(f"Error: Could not find location '{city} {state}'")
        return

    result = None
    for loc in geo_data["results"]:
        # Check if state name or abbreviation matches (e.g., "Tennessee" or "TN")
        # .get('admin1', '') safely gets the state name

        print(loc.get('name','').lower(),',', loc.get('admin1','').lower())
        if state.lower() in loc.get('admin1', '').lower() and city.lower() in loc.get('name', '').lower():
            result = loc
            break

    # Extract coordinates and location details
    if not result:
        print(f"Error: Could not find location '{city} {state}'")
        result = geo_data["results"][0]
    lat = result["latitude"]
    lon = result["longitude"]
    get_forecast(city_name, state_name, lat, lon)

def get_forecast(city, state, lat, lon):
    req = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min"], # Request daily variables
        "temperature_unit": "fahrenheit",
        "current_weather" : "true",
        "timezone": "auto" # Best practice: adjusts 'today' and 'tomorrow' to local time
    }

    url = "https://api.open-meteo.com/v1/forecast"
    response = requests.get(url, params=req)
    print(response.url)
    print(response.status_code)

    if response: # possible because the .__bool__() is overloaded
        data = response.json()
        date_tomorrow = data['daily']['time'][1]
        temp_max = data['daily']['temperature_2m_max'][1]
        temp_min = data['daily']['temperature_2m_min'][1]
        print(f"Forecast for {date_tomorrow} at {city}, {state}:")
        print(f"High: {temp_max}°F")
        print(f"Low: {temp_min}°F")
    else:
        raise Exception(f"Non-success status code: {response.status_code}")

if __name__ == "__main__":
    try:
        city_name = input("Enter city name: ")
        state_name = input("Enter state name: ")
        get_weather_by_city(city_name, state_name)
    except Exception as e:
        print(e)

def get_coordinates(city, state):
    """Converts City and State to Latitude/Longitude using Open-Meteo Geocoding API."""
    search_query = f"{city}, {state}"
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={search_query}&count=10&language=en&format=json"

    response = requests.get(geo_url)
    data = response.json()

    if "results" not in data:
        return None

    result = data["results"][0]
    return {
        "lat": result["latitude"],
        "lon": result["longitude"],
        "full_name": f"{result['name']}, {result.get('admin1', state)}"
    }
    return (lat,lon)

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if "results" not in data or len(data["results"]) == 0:
            return None

        location = data["results"][0]

        return (
            location["latitude"],
            location["longitude"],
            location["name"],
            location.get("admin1", state),
            location.get("timezone", "auto")
        )

    except requests.exceptions.RequestException:
        return None


def get_forecast(lat, lon, timezone):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "timezone": timezone,
        "forecast_days": 10
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if "error" in data:
            print("API Error:", data.get("reason"))
            return None

        if "daily" not in data:
            return None

        return data["daily"]

    except requests.exceptions.RequestException:
        return None


def display_forecast(city, state, daily):
    print(f"\n--- 10-Day Forecast for {city}, {state} ---")
    print("Date | Max Temp | Min Temp | Rain")
    print("-" * 50)

    for i in range(len(daily["time"])):
        print(
            f"{daily['time'][i]} | "
            f"{round(daily['temperature_2m_max'][i], 1)}°F | "
            f"{round(daily['temperature_2m_min'][i], 1)}°F | "
            f"{round(daily['precipitation_sum'][i], 3)}inch"
        )


coords = get_coordinates(city, state)

if not coords:
    print("Location not found.")
else:
    lat, lon, city_name, state_name, timezone = coords

    forecast = get_forecast(lat, lon, timezone)

    if forecast:
        display_forecast(city_name, state_name, forecast)
    else:
        print("Could not retrieve forecast.")
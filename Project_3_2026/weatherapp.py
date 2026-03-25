import requests

city = input("Enter city: ")
state = input("Enter state (full name): ")


def get_coordinates(city, state):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": f"{city}, {state}",
        "count": 1,
        "language": "en",
        "format": "json",
        "countryCode": "US"
    }

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
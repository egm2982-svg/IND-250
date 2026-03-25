import requests

def get_10_day_forecast(city, state):
    # Step 1: Get coordinates using the Geocoding API
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&admin1={state}&count=10&language=en&format=json"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()
    geo_params = {
        "name": f"{city}, {state}",
        "count": 1,
        "language": "en",
        "format": "json"
    }
    
    geo_res = requests.get(geo_url, params=geo_params).json()
    
    if "results" not in geo_res:
        return f"Error: Could not find coordinates for {city}, {state}."

    location = geo_res["results"][0]
    lat, lon = location["latitude"], location["longitude"]
    timezone = location.get("timezone", "auto")

    # Step 2: Fetch the 10-day forecast
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "forecast_days": 10,
        "timezone": timezone
    }
    
    weather_res = requests.get(weather_url, params=weather_params).json()
    daily_data = weather_res.get("daily", {})

    # Print the formatted results
    print(f"\n10-Day Forecast for {location['name']}, {location.get('admin1', state)}:")
    print("-" * 50)
    for i in range(len(daily_data.get("time", []))):
        date = daily_data["time"][i]
        t_max = daily_data["temperature_2m_max"][i]
        t_min = daily_data["temperature_2m_min"][i]
        precip = daily_data["precipitation_sum"][i]
        print(f"{date} | Max: {t_max}°C | Min: {t_min}°C | Rain: {precip}mm")

# Run the query
user_city = input("Enter City: ")
user_state = input("Enter State: ")
get_10_day_forecast(user_city, user_state)
